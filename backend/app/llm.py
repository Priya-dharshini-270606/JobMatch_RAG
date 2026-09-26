import os
from groq import Groq
from dotenv import load_dotenv


# Load .env file
load_dotenv()


# Get API key
api_key = os.getenv("GROQ_API_KEY")


# Check API key
if not api_key:
    raise ValueError(
        "GROQ_API_KEY is not set. "
        "Please add it to backend/.env"
    )


# Create Groq client
client = Groq(
    api_key=api_key
)


def analyze_requirement(
    requirement,
    evidence,
    status,
    evidence_type="Unknown",
    matched_terms=None
):

    if matched_terms is None:
        matched_terms = []


    prompt = f"""
You are an evidence-grounded AI job matching assistant.

Your task is to analyze ONE job requirement using ONLY
the resume evidence provided below.

IMPORTANT RULES:

1. Use only the provided resume evidence.
2. Do not invent skills, tools, projects, experience,
   certifications, years of experience, or proficiency.
3. Do not assume that a technology was actually implemented
   unless the evidence explicitly supports that claim.
4. If the evidence comes from the Technical Skills section,
   say that the resume lists the skill.
5. If the evidence comes from a Project/Experience section,
   describe only what is explicitly stated there.
6. Do not claim that something is production-ready,
   industry-level, advanced, or expert unless the evidence
   explicitly says so.
7. Do not recommend unnecessary technologies.
8. Recommendations should be directly related to the
   job requirement and the available resume evidence.
9. If there is insufficient evidence, clearly say so.
10. Do not change the match status.

Job Requirement:
{requirement}

Match Status:
{status}

Evidence Type:
{evidence_type}

Related Matched Terms:
{", ".join(matched_terms) if matched_terms else "None"}

Resume Evidence:
{evidence}

Return exactly in this format:

Explanation:
<brief explanation of how the resume evidence relates
to the job requirement>

Evidence:
<only the specific evidence supported by the resume>

Recommendation:
<specific improvement if needed, otherwise "No improvement needed">
"""


    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )


    return response.choices[0].message.content