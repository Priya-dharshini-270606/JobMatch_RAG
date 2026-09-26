import re


def split_into_sections(text: str):
    sections = re.split(
        r'\n(?=Education|Experience|Projects|Technical Skills|Achievements & Certifications)',
        text
    )

    chunks = []

    for section in sections:
        section = section.strip()

        if not section:
            continue

        if section.startswith("Projects"):
            project_chunks = split_projects(section)
            chunks.extend(project_chunks)
        else:
            chunks.append(section)

    return chunks


def split_projects(project_section: str):
    project_text = project_section.replace("Projects\n", "", 1).strip()

    projects = re.split(
        r'\n(?=•[A-Za-z])',
        project_text
    )

    chunks = []

    for project in projects:
        project = project.strip()

        if project:
            chunks.append("Project\n" + project)

    return chunks