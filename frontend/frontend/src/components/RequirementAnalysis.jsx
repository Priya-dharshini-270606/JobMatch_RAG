import { useState } from "react";
import EvidenceCard from "./EvidenceCard.jsx";

function RequirementAnalysis({ evidence }) {
  const [showAnalysis, setShowAnalysis] = useState(false);

  return (
    <section className="requirement-analysis-section">

      {!showAnalysis ? (

        <div className="requirement-analysis-card">

          <div className="requirement-analysis-icon">
            ✓
          </div>

          <div className="requirement-analysis-content">

            <div>
              <p className="section-label">
                DETAILED INSIGHTS
              </p>

              <h3>
                Explore Requirement Analysis
              </h3>

              <p>
                See how each job requirement matches
                your resume, with supporting evidence
                and AI-generated analysis.
              </p>
            </div>

            <button
              className="requirement-analysis-button"
              onClick={() => setShowAnalysis(true)}
            >
              View Details
              <span>→</span>
            </button>

          </div>

        </div>

      ) : (

        <div className="requirement-analysis-expanded">

          <div className="requirement-analysis-header">

            <div>
              <p className="section-label">
                DETAILED INSIGHTS
              </p>

              <h2>
                Requirement Analysis
              </h2>

              <p>
                Review the evidence behind each
                requirement match.
              </p>
            </div>

            <button
              className="close-analysis-button"
              onClick={() => setShowAnalysis(false)}
            >
              Hide
            </button>

          </div>


          <div className="evidence-list">

            {evidence.map((item, index) => (
              <EvidenceCard
                key={index}
                item={item}
              />
            ))}

          </div>

        </div>

      )}

    </section>
  );
}

export default RequirementAnalysis;