def clean_job_description(text: str) -> str:
    """
    Clean the job description text.
    """

    text = text.strip()

    # Remove excessive blank lines
    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)