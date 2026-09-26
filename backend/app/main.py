from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.resume_parser import extract_text_from_pdf
from app.chunker import split_into_sections

from app.embedding import (
    generate_embeddings,
    generate_query_embedding
)

from app.vector_store import (
    store_resume_chunks,
    search_resume
)

from app.jd_parser import extract_requirement_details
from app.matcher import classify_match
from app.llm import analyze_requirement
from app.report_generator import generate_job_match_report


# ==================================================
# FastAPI Application
# ==================================================

app = FastAPI(title="JobMatch RAG")


# ==================================================
# CORS Configuration
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# Models
# ==================================================

class JobDescription(BaseModel):
    text: str


# ==================================================
# Home
# ==================================================

@app.get("/")
def home():

    return {
        "message": "JobMatch RAG Backend is running!"
    }


# ==================================================
# Upload Resume
# ==================================================

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:

        buffer.write(
            await file.read()
        )

    # ----------------------------------------------
    # Extract text from PDF
    # ----------------------------------------------

    extracted_text = extract_text_from_pdf(
        file_path
    )

    # ----------------------------------------------
    # Split resume into sections/chunks
    # ----------------------------------------------

    chunks = split_into_sections(
        extracted_text
    )

    # ----------------------------------------------
    # Generate embeddings
    # ----------------------------------------------

    embeddings = generate_embeddings(
        chunks
    )

    # ----------------------------------------------
    # Store in ChromaDB
    # ----------------------------------------------

    stored_count = store_resume_chunks(
        chunks,
        embeddings
    )

    return {

        "filename": file.filename,

        "number_of_chunks": len(chunks),

        "embedding_dimension": len(
            embeddings[0]
        ),

        "stored_in_chromadb": stored_count
    }


# ==================================================
# Search Resume
# ==================================================

@app.get("/search-resume")
def search_resume_endpoint(
    query: str,
    top_k: int = 7
):

    # ----------------------------------------------
    # Generate query embedding
    # ----------------------------------------------

    query_embedding = generate_query_embedding(
        query
    )

    # ----------------------------------------------
    # Search ChromaDB
    # ----------------------------------------------

    results = search_resume(
        query_embedding,
        top_k
    )

    return {

        "query": query,

        "results": results
    }


# ==================================================
# Upload Job Description
# ==================================================

@app.post("/upload-job-description")
def upload_job_description(
    job: JobDescription
):

    cleaned_text = job.text.strip()

    return {

        "message":
            "Job description received successfully",

        "job_description":
            cleaned_text
    }


# ==================================================
# Match Job Description with Resume
# ==================================================

@app.post("/match-job")
def match_job(
    job: JobDescription
):

    # ==================================================
    # Step 1: Extract Requirements
    # ==================================================

    requirement_details = extract_requirement_details(
        job.text
    )

    required_requirements = (
        requirement_details["required"]
    )

    preferred_requirements = (
        requirement_details["preferred"]
    )

    all_requirements = (
        required_requirements
        + preferred_requirements
    )

    matches = []


    # ==================================================
    # Step 2: Match Every Requirement
    # ==================================================

    for requirement in all_requirements:

        # ----------------------------------------------
        # Generate requirement embedding
        # ----------------------------------------------

        query_embedding = generate_query_embedding(
            requirement
        )

        # ----------------------------------------------
        # Retrieve resume evidence
        # ----------------------------------------------

        results = search_resume(
            query_embedding,
            top_k=7
        )

        documents = results.get(
            "documents",
            [[]]
        )

        distances = results.get(
            "distances",
            [[]]
        )


        # ----------------------------------------------
        # Determine requirement type
        # ----------------------------------------------

        if requirement in required_requirements:

            requirement_type = "Required"

        else:

            requirement_type = "Preferred"


        # ==================================================
        # Resume Evidence Found
        # ==================================================

        if documents and documents[0]:

            documents_list = documents[0]

            distances_list = distances[0]


            # ----------------------------------------------
            # Classify Match
            # ----------------------------------------------

            match_result = classify_match(
                requirement,
                documents_list,
                distances_list
            )


            # ----------------------------------------------
            # Grounded LLM Analysis
            # ----------------------------------------------

            llm_analysis = analyze_requirement(

                requirement=requirement,

                evidence=match_result["evidence"],

                status=match_result["status"],

                evidence_type=match_result[
                    "evidence_type"
                ],

                matched_terms=match_result[
                    "matched_terms"
                ]
            )


            # ----------------------------------------------
            # Store Match Result
            # ----------------------------------------------

            matches.append({

                "requirement":
                    requirement,

                "type":
                    requirement_type,

                "status":
                    match_result["status"],

                "match_score":
                    match_result["match_score"],

                "evidence_type":
                    match_result["evidence_type"],

                "evidence":
                    match_result["evidence"],

                "distance":
                    match_result["distance"],

                "matched_terms":
                    match_result["matched_terms"],

                "llm_analysis":
                    llm_analysis
            })


        # ==================================================
        # No Resume Evidence
        # ==================================================

        else:

            llm_analysis = analyze_requirement(

                requirement=requirement,

                evidence=
                    "No relevant resume evidence found.",

                status="Missing",

                evidence_type="No Evidence",

                matched_terms=[]
            )


            matches.append({

                "requirement":
                    requirement,

                "type":
                    requirement_type,

                "status":
                    "Missing",

                "match_score":
                    0,

                "evidence_type":
                    "No Evidence",

                "evidence":
                    None,

                "distance":
                    None,

                "matched_terms":
                    [],

                "llm_analysis":
                    llm_analysis
            })


    # ==================================================
    # Step 3: Separate Required and Preferred
    # ==================================================

    required_matches = [

        match
        for match in matches

        if match["type"] == "Required"
    ]

    preferred_matches = [

        match
        for match in matches

        if match["type"] == "Preferred"
    ]


    # ==================================================
    # Step 4: Required Statistics
    # ==================================================

    required_matched = sum(

        1

        for match in required_matches

        if match["status"] == "Matched"
    )

    required_partial = sum(

        1

        for match in required_matches

        if match["status"] == "Partial"
    )

    required_missing = sum(

        1

        for match in required_matches

        if match["status"] == "Missing"
    )


    # ==================================================
    # Step 5: Preferred Statistics
    # ==================================================

    preferred_matched = sum(

        1

        for match in preferred_matches

        if match["status"] == "Matched"
    )

    preferred_partial = sum(

        1

        for match in preferred_matches

        if match["status"] == "Partial"
    )

    preferred_missing = sum(

        1

        for match in preferred_matches

        if match["status"] == "Missing"
    )


    # ==================================================
    # Step 6: Calculate Required Score
    # ==================================================

    required_score = 0

    if required_matches:

        required_score = (

            sum(
                match["match_score"]
                for match in required_matches
            )

            / len(required_matches)
        )


    # ==================================================
    # Calculate Preferred Score
    # ==================================================

    preferred_score = 0

    if preferred_matches:

        preferred_score = (

            sum(
                match["match_score"]
                for match in preferred_matches
            )

            / len(preferred_matches)
        )


    # ==================================================
    # Step 7: Weighted Overall Score
    # ==================================================

    if (
        required_matches
        and preferred_matches
    ):

        overall_score = (

            required_score * 0.80

            + preferred_score * 0.20
        )

    elif required_matches:

        overall_score = required_score

    elif preferred_matches:

        overall_score = preferred_score

    else:

        overall_score = 0


    # ==================================================
    # Step 8: Overall Statistics
    # ==================================================

    matched_count = sum(

        1

        for match in matches

        if match["status"] == "Matched"
    )

    partial_count = sum(

        1

        for match in matches

        if match["status"] == "Partial"
    )

    missing_count = sum(

        1

        for match in matches

        if match["status"] == "Missing"
    )


    # ==================================================
    # Step 9: Generate Final JobMatch Report
    # ==================================================

    report = generate_job_match_report(

        job_description=job.text,

        requirements_extracted=
            requirement_details,

        matches=matches
    )


    # ==================================================
    # Step 10: Preserve Weighted Scores
    # ==================================================

    report[
        "overall_summary"
    ][
        "overall_match_percentage"
    ] = round(
        overall_score,
        2
    )


    report[
        "required_summary"
    ][
        "score"
    ] = round(
        required_score,
        2
    )


    report[
        "preferred_summary"
    ][
        "score"
    ] = round(
        preferred_score,
        2
    )


    # ==================================================
    # Update Overall Counts
    # ==================================================

    report[
        "overall_summary"
    ][
        "matched"
    ] = matched_count

    report[
        "overall_summary"
    ][
        "partial"
    ] = partial_count

    report[
        "overall_summary"
    ][
        "missing"
    ] = missing_count


    # ==================================================
    # Final Response
    # ==================================================

    return report