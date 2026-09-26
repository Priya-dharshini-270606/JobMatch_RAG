import re


def split_into_sections(text: str):
    sections = re.split(
        r'\n(?=Education|Experience|Projects|Technical Skills|Achievements & Certifications)',
        text
    )

    chunks = []

    for section in sections:
        section = section.strip()

        if section:
            chunks.append(section)

    return chunks