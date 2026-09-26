# ==========================================================
# JobMatch RAG - Final Report Generator
# ==========================================================


def generate_job_match_report(
    job_description,
    requirements_extracted,
    matches
):
    """
    Generate a clean structured JobMatch report
    from the existing matching results.
    """

    # ======================================================
    # Separate Required and Preferred
    # ======================================================

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


    # ======================================================
    # Calculate Summary
    # ======================================================

    total_requirements = len(matches)

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


    # ======================================================
    # Calculate Overall Match Percentage
    # ======================================================

    if total_requirements > 0:

        overall_match_percentage = round(
            sum(
                match["match_score"]
                for match in matches
            ) / total_requirements,
            2
        )

    else:

        overall_match_percentage = 0


    # ======================================================
    # Required Summary
    # ======================================================

    required_total = len(required_matches)

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

    if required_total > 0:

        required_score = round(
            sum(
                match["match_score"]
                for match in required_matches
            ) / required_total,
            2
        )

    else:

        required_score = 0


    # ======================================================
    # Preferred Summary
    # ======================================================

    preferred_total = len(preferred_matches)

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

    if preferred_total > 0:

        preferred_score = round(
            sum(
                match["match_score"]
                for match in preferred_matches
            ) / preferred_total,
            2
        )

    else:

        preferred_score = 0


    # ======================================================
    # Skill Lists
    # ======================================================

    matched_skills = [
        match["requirement"]
        for match in matches
        if match["status"] == "Matched"
    ]

    partial_skills = [
        match["requirement"]
        for match in matches
        if match["status"] == "Partial"
    ]

    missing_skills = [
        match["requirement"]
        for match in matches
        if match["status"] == "Missing"
    ]


    # ======================================================
    # Detailed Evidence
    # ======================================================

    evidence_details = []

    for match in matches:

        evidence_details.append({

            "requirement": match["requirement"],

            "type": match["type"],

            "status": match["status"],

            "match_score": match["match_score"],

            "evidence_type": match["evidence_type"],

            "matched_terms": match.get(
                "matched_terms",
                []
            ),

            "evidence": match.get(
                "evidence"
            ),

            "analysis": match.get(
                "llm_analysis"
            )

        })


    # ======================================================
    # Recommendations
    # ======================================================

    recommendations = []

    for match in matches:

        if match["status"] == "Missing":

            recommendations.append(
                f"Consider developing experience in "
                f"{match['requirement']}."
            )

        elif match["status"] == "Partial":

            recommendations.append(
                f"Strengthen evidence for "
                f"{match['requirement']} by adding "
                f"a relevant project, implementation detail, "
                f"or measurable experience."
            )


    # Remove duplicate recommendations

    recommendations = list(
        dict.fromkeys(recommendations)
    )


    # ======================================================
    # Final Report
    # ======================================================

    report = {

        "report_title": "JobMatch RAG Report",

        "job_description": job_description,

        "requirements": {

            "required": requirements_extracted.get(
                "required",
                []
            ),

            "preferred": requirements_extracted.get(
                "preferred",
                []
            )

        },

        "overall_summary": {

            "overall_match_percentage":
                overall_match_percentage,

            "total_requirements":
                total_requirements,

            "matched":
                matched_count,

            "partial":
                partial_count,

            "missing":
                missing_count

        },

        "required_summary": {

            "total":
                required_total,

            "matched":
                required_matched,

            "partial":
                required_partial,

            "missing":
                required_missing,

            "score":
                required_score

        },

        "preferred_summary": {

            "total":
                preferred_total,

            "matched":
                preferred_matched,

            "partial":
                preferred_partial,

            "missing":
                preferred_missing,

            "score":
                preferred_score

        },

        "skill_summary": {

            "matched":
                matched_skills,

            "partial":
                partial_skills,

            "missing":
                missing_skills

        },

        "recommendations":
            recommendations,

        "evidence":
            evidence_details

    }


    return report