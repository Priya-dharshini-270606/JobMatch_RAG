import { jsPDF } from "jspdf";

function ReportDownload({ report }) {
  const downloadReport = () => {
    if (!report) return;

    const pdf = new jsPDF();

    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();

    const margin = 15;
    const maxWidth = pageWidth - margin * 2;

    let y = 20;

    const addText = (text, size = 10, bold = false) => {
      pdf.setFont("helvetica", bold ? "bold" : "normal");
      pdf.setFontSize(size);

      const lines = pdf.splitTextToSize(
        String(text || ""),
        maxWidth
      );

      for (const line of lines) {
        if (y > pageHeight - 20) {
          pdf.addPage();
          y = 20;
        }

        pdf.text(line, margin, y);
        y += size * 0.55;
      }

      y += 4;
    };

    const addHeading = (text) => {
      if (y > pageHeight - 35) {
        pdf.addPage();
        y = 20;
      }

      pdf.setFont("helvetica", "bold");
      pdf.setFontSize(14);
      pdf.text(text, margin, y);

      y += 9;
    };

    // =========================================
    // TITLE
    // =========================================

    pdf.setFont("helvetica", "bold");
    pdf.setFontSize(22);

    pdf.text("JobMatch RAG Report", margin, y);

    y += 12;

    pdf.setFont("helvetica", "normal");
    pdf.setFontSize(10);

    pdf.text(
      "AI-powered Resume and Job Description Analysis",
      margin,
      y
    );

    y += 15;

    // =========================================
    // OVERALL SUMMARY
    // =========================================

    addHeading("Overall Match");

    const overall = report.overall_summary || {};

    addText(
      `Overall Match: ${overall.overall_match_percentage ?? 0}%`,
      12,
      true
    );

    addText(
      `Total Requirements: ${overall.total_requirements ?? 0}`
    );

    addText(
      `Matched: ${overall.matched ?? 0}`
    );

    addText(
      `Partial: ${overall.partial ?? 0}`
    );

    addText(
      `Missing: ${overall.missing ?? 0}`
    );

    // =========================================
    // REQUIRED
    // =========================================

    addHeading("Required Requirements");

    const required = report.required_summary || {};

    addText(
      `Score: ${required.score ?? 0}%`,
      11,
      true
    );

    addText(
      `Matched: ${required.matched ?? 0}`
    );

    addText(
      `Partial: ${required.partial ?? 0}`
    );

    addText(
      `Missing: ${required.missing ?? 0}`
    );

    // =========================================
    // PREFERRED
    // =========================================

    addHeading("Preferred Requirements");

    const preferred = report.preferred_summary || {};

    addText(
      `Score: ${preferred.score ?? 0}%`,
      11,
      true
    );

    addText(
      `Matched: ${preferred.matched ?? 0}`
    );

    addText(
      `Partial: ${preferred.partial ?? 0}`
    );

    addText(
      `Missing: ${preferred.missing ?? 0}`
    );

    // =========================================
    // SKILLS
    // =========================================

    addHeading("Skill Summary");

    const skills = report.skill_summary || {};

    addText(
      `Matched Skills: ${(skills.matched || []).join(", ") || "None"}`
    );

    addText(
      `Partial Skills: ${(skills.partial || []).join(", ") || "None"}`
    );

    addText(
      `Missing Skills: ${(skills.missing || []).join(", ") || "None"}`
    );

    // =========================================
    // RECOMMENDATIONS
    // =========================================

    addHeading("Recommendations");

    if (
      report.recommendations &&
      report.recommendations.length > 0
    ) {
      report.recommendations.forEach(
        (recommendation, index) => {
          addText(
            `${index + 1}. ${recommendation}`
          );
        }
      );
    } else {
      addText("No recommendations.");
    }

    // =========================================
    // REQUIREMENT ANALYSIS
    // =========================================

    addHeading("Detailed Requirement Analysis");

    const evidence = report.evidence || [];

    evidence.forEach((item, index) => {

      addHeading(
        `${index + 1}. ${item.requirement || "Requirement"}`
      );

      addText(
        `Type: ${item.type || "Unknown"}`,
        10,
        true
      );

      addText(
        `Status: ${item.status || "Unknown"}`,
        10,
        true
      );

      addText(
        `Match Score: ${item.match_score ?? 0}%`
      );

      addText(
        `Evidence Type: ${item.evidence_type || "Unknown"}`
      );

      if (item.matched_terms?.length) {
        addText(
          `Matched Terms: ${item.matched_terms.join(", ")}`
        );
      }

      addText("Resume Evidence:", 10, true);

      addText(
        item.evidence || "No evidence found."
      );

      addText("AI Analysis:", 10, true);

      addText(
        item.llm_analysis || "No AI analysis available."
      );

      y += 5;
    });

    // =========================================
    // FOOTER
    // =========================================

    const totalPages =
      pdf.internal.getNumberOfPages();

    for (let page = 1; page <= totalPages; page++) {
      pdf.setPage(page);

      pdf.setFont("helvetica", "normal");
      pdf.setFontSize(8);

      pdf.text(
        `JobMatch RAG • Page ${page} of ${totalPages}`,
        margin,
        pageHeight - 8
      );
    }

    pdf.save("JobMatch_RAG_Report.pdf");
  };

  return (
    <button
      className="download-report-button"
      onClick={downloadReport}
      disabled={!report}
    >
      ↓ Download Full Report
    </button>
  );
}

export default ReportDownload;