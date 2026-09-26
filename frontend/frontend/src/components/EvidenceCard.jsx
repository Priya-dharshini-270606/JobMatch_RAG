import { useState } from "react";

function EvidenceCard({ item }) {
  const [isOpen, setIsOpen] = useState(false);

  const status = item.status?.toLowerCase() || "missing";

  return (
    <div className={`evidence-card ${status}`}>

      <div
        className="evidence-card-header"
        onClick={() => setIsOpen(!isOpen)}
      >

        <div className="requirement-left">

          <div className="requirement-icon">
            {status === "matched"
              ? "✓"
              : status === "partial"
              ? "~"
              : "!"}
          </div>

          <div className="requirement-info">
            <h3>{item.requirement}</h3>

            <span className="requirement-type">
              {item.type || "Required requirement"}
            </span>
          </div>

        </div>


        <div className="requirement-right">

          <span className={`status-badge ${status}`}>
            {item.status}
          </span>

          <span className="match-score">
            {item.match_score ?? 0}%
          </span>

          <div className={`expand-icon ${isOpen ? "open" : ""}`}>
            ↓
          </div>

        </div>

      </div>


      {isOpen && (
        <div className="evidence-card-body">

          <div className="detail-row">

            <div className="detail-item">

              <span className="detail-label">
                EVIDENCE TYPE
              </span>

              <span className="detail-value">
                {item.evidence_type || "No evidence"}
              </span>

            </div>


            {item.matched_terms &&
              item.matched_terms.length > 0 && (

                <div className="detail-item">

                  <span className="detail-label">
                    MATCHED TERMS
                  </span>

                  <div className="matched-terms">

                    {item.matched_terms.map(
                      (term, index) => (
                        <span
                          key={index}
                          className="matched-term"
                        >
                          {term}
                        </span>
                      )
                    )}

                  </div>

                </div>

              )}

          </div>


          <div className="evidence-detail-section">

            <span className="detail-label">
              RESUME EVIDENCE
            </span>

            <div className="evidence-content">

              {item.evidence ||
                "No relevant resume evidence found."}

            </div>

          </div>


          <div className="evidence-detail-section">

            <span className="detail-label">
              AI ANALYSIS
            </span>

            <div className="ai-analysis-content">

              {item.llm_analysis ||
                item.analysis ||
                "No AI analysis available."}

            </div>

          </div>

        </div>
      )}

    </div>
  );
}

export default EvidenceCard;