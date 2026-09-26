import re


KNOWN_SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "TypeScript",
    "React",
    "Node.js",
    "FastAPI",
    "Flask",
    "Django",
    "REST APIs",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "AWS",
    "Azure",
    "GCP",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "Machine Learning",
    "Deep Learning",
    "Generative AI",
    "LLM",
    "LLMs",
    "RAG",
    "LangChain",
    "LlamaIndex",
    "ChromaDB",
    "Vector Databases",
    "Vector Database",
    "Embeddings",
    "NLP",
    "Computer Vision",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Data Analysis",
    "Data Structures",
    "Algorithms",
    "OOPS",
    "Object Oriented Programming"
]


# --------------------------------------------------
# Extract all skills from JD
# --------------------------------------------------

def extract_requirements(job_description: str):

    found_skills = []

    text = job_description.lower()

    for skill in KNOWN_SKILLS:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


# --------------------------------------------------
# Split JD into sentences
# --------------------------------------------------

def split_into_sentences(text: str):

    sentences = re.split(
        r'(?<=[.!?])\s+|\n+',
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


# --------------------------------------------------
# Detect preferred requirements
# --------------------------------------------------

def extract_requirement_details(job_description: str):

    all_requirements = extract_requirements(
        job_description
    )

    sentences = split_into_sentences(
        job_description
    )

    preferred_keywords = [
        "preferred",
        "prefer",
        "nice to have",
        "nice-to-have",
        "plus",
        "bonus",
        "good to have",
        "good-to-have",
        "desired",
        "optional"
    ]

    preferred_requirements = []
    required_requirements = []

    for skill in all_requirements:

        skill_lower = skill.lower()

        skill_sentences = []

        # Find the sentence containing the skill
        for sentence in sentences:

            if re.search(
                r"\b" + re.escape(skill_lower) + r"\b",
                sentence.lower()
            ):
                skill_sentences.append(sentence.lower())

        is_preferred = False

        # Check only the sentence containing the skill
        for sentence in skill_sentences:

            if any(
                keyword in sentence
                for keyword in preferred_keywords
            ):
                is_preferred = True
                break

        if is_preferred:
            preferred_requirements.append(skill)

        else:
            required_requirements.append(skill)

    return {
        "required": required_requirements,
        "preferred": preferred_requirements
    }


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    jd = """
    We are looking for an AI Developer with strong Python programming,
    Machine Learning, Generative AI, RAG, LangChain and FastAPI experience.
    Knowledge of AWS, Docker and vector databases is preferred.
    """

    details = extract_requirement_details(jd)

    print("Required:")
    print(details["required"])

    print()

    print("Preferred:")
    print(details["preferred"])