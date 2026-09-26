import re


# ==================================================
# Related Technology Mappings
# ==================================================

RELATED_SKILLS = {

    "vector databases": [
        "chromadb",
        "pinecone",
        "faiss",
        "milvus",
        "qdrant",
        "weaviate",
        "vector database",
        "vector databases"
    ],

    "machine learning": [
        "machine learning",
        "scikit-learn",
        "sklearn",
        "random forest",
        "decision tree",
        "logistic regression",
        "linear regression",
        "classification",
        "regression",
        "clustering"
    ],

    "deep learning": [
        "deep learning",
        "pytorch",
        "tensorflow",
        "keras",
        "neural network",
        "cnn",
        "rnn",
        "lstm"
    ],

    "generative ai": [
        "generative ai",
        "llm",
        "llms",
        "large language model",
        "gpt",
        "groq",
        "transformers",
        "hugging face",
        "text generation",
        "ai assistant"
    ],

    "rag": [
        "rag",
        "retrieval augmented generation",
        "retrieval-augmented generation",
        "retrieval",
        "vector retrieval",
        "semantic retrieval"
    ],

    "rest apis": [
        "rest api",
        "rest apis",
        "api",
        "apis",
        "fastapi",
        "flask",
        "express",
        "node.js",
        "nodejs"
    ],

    "python": [
        "python"
    ],

    "fastapi": [
        "fastapi"
    ],

    "aws": [
        "aws",
        "amazon web services",
        "ec2",
        "s3",
        "rds",
        "lambda"
    ],

    "docker": [
        "docker",
        "dockerfile",
        "docker compose",
        "docker-compose",
        "container",
        "containers"
    ],

    "langchain": [
        "langchain"
    ],

    "embeddings": [
        "embeddings",
        "embedding",
        "sentence transformers",
        "sentence-transformers"
    ],

    "nlp": [
        "nlp",
        "natural language processing",
        "text classification",
        "tokenization",
        "lemmatization",
        "named entity recognition"
    ],

    "data analysis": [
        "data analysis",
        "pandas",
        "numpy",
        "matplotlib",
        "data visualization",
        "data preprocessing"
    ],

    "data structures": [
        "data structures",
        "arrays",
        "linked lists",
        "stacks",
        "queues",
        "trees",
        "graphs",
        "hash tables"
    ],

    "algorithms": [
        "algorithms",
        "sorting",
        "searching",
        "binary search",
        "dynamic programming",
        "recursion",
        "greedy"
    ]
}


# ==================================================
# Normalize Text
# ==================================================

def normalize_text(text):
    """
    Normalize text for reliable matching.
    """

    text = text.lower()

    # Normalize different dash characters
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==================================================
# Exact Term Matching
# ==================================================

def contains_term(document, term):
    """
    Check whether a complete term exists in a document.

    Uses word boundaries instead of simple substring matching.
    """

    document = normalize_text(document)
    term = normalize_text(term)

    pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"

    return re.search(pattern, document) is not None


# ==================================================
# Find Related Evidence
# ==================================================

def find_related_evidence(requirement, document):

    requirement_lower = normalize_text(
        requirement
    )

    related_terms = RELATED_SKILLS.get(
        requirement_lower,
        []
    )

    matched_terms = []

    for term in related_terms:

        if contains_term(
            document,
            term
        ):

            matched_terms.append(term)

    return matched_terms


# ==================================================
# Identify Section Type
# ==================================================

def is_project_or_experience(document):

    document_lower = normalize_text(
        document
    )

    return (
        document_lower.startswith("project")
        or document_lower.startswith("experience")
        or "\nproject" in document_lower
        or "\nexperience" in document_lower
    )


def is_technical_skills(document):

    document_lower = normalize_text(
        document
    )

    return (
        "technical skills" in document_lower
        or document_lower.startswith("skills")
    )


def is_profile(document):

    document_lower = normalize_text(
        document
    )

    return (
        document_lower.startswith("objective")
        or document_lower.startswith("summary")
        or document_lower.startswith("profile")
        or "objective" in document_lower
        or "summary" in document_lower
    )


# ==================================================
# Classify Match
# ==================================================

def classify_match(
    requirement,
    documents,
    distances
):
    """
    Classify a job requirement based on resume evidence.

    Evidence hierarchy:

    1. Direct project/experience
       -> Matched (100)

    2. Related technology in project/experience
       -> Matched (90)

    3. Direct technical skill
       -> Partial (70)

    4. Related technology in technical skills
       -> Partial (60)

    5. Direct profile/objective evidence
       -> Partial (40)

    6. Strong semantic evidence
       -> Partial (60)

    7. Moderate semantic evidence
       -> Partial (40)

    8. No meaningful evidence
       -> Missing (0)
    """

    # --------------------------------------------------
    # No documents
    # --------------------------------------------------

    if not documents:

        return {
            "status": "Missing",
            "evidence": None,
            "distance": None,
            "match_score": 0,
            "evidence_type": "No Evidence",
            "matched_terms": []
        }


    requirement_lower = normalize_text(
        requirement
    )


    # ==================================================
    # 1. DIRECT PROJECT / EXPERIENCE
    # ==================================================

    project_candidates = []

    for i, document in enumerate(documents):

        if not is_project_or_experience(
            document
        ):
            continue

        if contains_term(
            document,
            requirement_lower
        ):

            project_candidates.append(i)


    if project_candidates:

        # Select closest semantic result
        best_index = min(
            project_candidates,
            key=lambda i: distances[i]
        )

        return {
            "status": "Matched",
            "evidence": documents[best_index],
            "distance": distances[best_index],
            "match_score": 100,
            "evidence_type": "Project/Experience",
            "matched_terms": [requirement]
        }


    # ==================================================
    # 2. RELATED TECHNOLOGY IN PROJECT / EXPERIENCE
    # ==================================================

    related_candidates = []

    for i, document in enumerate(documents):

        if not is_project_or_experience(
            document
        ):
            continue

        related_terms = find_related_evidence(
            requirement,
            document
        )

        if related_terms:

            related_candidates.append(
                (
                    i,
                    related_terms
                )
            )


    if related_candidates:

        best_index, matched_terms = min(
            related_candidates,
            key=lambda item: distances[item[0]]
        )

        return {
            "status": "Matched",
            "evidence": documents[best_index],
            "distance": distances[best_index],
            "match_score": 90,
            "evidence_type": "Related Project/Experience",
            "matched_terms": matched_terms
        }


    # ==================================================
    # 3. DIRECT TECHNICAL SKILL
    # ==================================================

    technical_candidates = []

    for i, document in enumerate(documents):

        if not is_technical_skills(
            document
        ):
            continue

        if contains_term(
            document,
            requirement_lower
        ):

            technical_candidates.append(i)


    if technical_candidates:

        best_index = min(
            technical_candidates,
            key=lambda i: distances[i]
        )

        return {
            "status": "Partial",
            "evidence": documents[best_index],
            "distance": distances[best_index],
            "match_score": 70,
            "evidence_type": "Technical Skills",
            "matched_terms": [requirement]
        }


    # ==================================================
    # 4. RELATED TECHNOLOGY IN TECHNICAL SKILLS
    # ==================================================

    related_skill_candidates = []

    for i, document in enumerate(documents):

        if not is_technical_skills(
            document
        ):
            continue

        related_terms = find_related_evidence(
            requirement,
            document
        )

        if related_terms:

            related_skill_candidates.append(
                (
                    i,
                    related_terms
                )
            )


    if related_skill_candidates:

        best_index, matched_terms = min(
            related_skill_candidates,
            key=lambda item: distances[item[0]]
        )

        return {
            "status": "Partial",
            "evidence": documents[best_index],
            "distance": distances[best_index],
            "match_score": 60,
            "evidence_type": "Related Technical Skill",
            "matched_terms": matched_terms
        }


    # ==================================================
    # 5. OBJECTIVE / PROFILE
    # ==================================================

    profile_candidates = []

    for i, document in enumerate(documents):

        if not is_profile(
            document
        ):
            continue

        if contains_term(
            document,
            requirement_lower
        ):

            profile_candidates.append(i)


    if profile_candidates:

        best_index = min(
            profile_candidates,
            key=lambda i: distances[i]
        )

        return {
            "status": "Partial",
            "evidence": documents[best_index],
            "distance": distances[best_index],
            "match_score": 40,
            "evidence_type": "Objective/Profile",
            "matched_terms": [requirement]
        }


    # ==================================================
    # 6. SEMANTIC EVIDENCE
    # ==================================================

    if distances:

        best_index = min(
            range(len(distances)),
            key=lambda i: distances[i]
        )

        best_distance = distances[
            best_index
        ]

        best_document = documents[
            best_index
        ]


        if best_distance < 1.0:

            return {
                "status": "Partial",
                "evidence": best_document,
                "distance": best_distance,
                "match_score": 60,
                "evidence_type": "Semantic Evidence",
                "matched_terms": []
            }


        elif best_distance < 1.5:

            return {
                "status": "Partial",
                "evidence": best_document,
                "distance": best_distance,
                "match_score": 40,
                "evidence_type": "Semantic Evidence",
                "matched_terms": []
            }


    # ==================================================
    # 7. NO MEANINGFUL EVIDENCE
    # ==================================================

    return {
        "status": "Missing",
        "evidence": documents[0],
        "distance": distances[0] if distances else None,
        "match_score": 0,
        "evidence_type": "No Strong Evidence",
        "matched_terms": []
    }