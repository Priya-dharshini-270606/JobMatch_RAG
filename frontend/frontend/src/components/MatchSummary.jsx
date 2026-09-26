function MatchSummary({ summary }) {
  if (!summary) {
    return null;
  }

  const score = summary.overall_match_percentage ?? 0;

  return (
    <section className="match-summary">

      {/* Overall Score */}
      <div className="summary-main">

        <div className="summary-title-row">
          <div>
            <p className="section-label">
              OVERALL MATCH
            </p>

            <h2 className="summary-heading">
              Resume Compatibility
            </h2>
          </div>

          <div className="score-badge">
            AI
          </div>
        </div>

        <div className="overall-score">
          {score}%
        </div>

        <div className="score-bar">
          <div
            className="score-bar-fill"
            style={{ width: `${Math.min(score, 100)}%` }}
          />
        </div>

        <p className="summary-text">
          Based on the requirements identified from the
          job description and evidence retrieved from your
          resume.
        </p>

      </div>


      {/* Statistics */}
      <div className="summary-stats">

        <div className="summary-stat">
          <span className="stat-number matched-number">
            {summary.matched ?? 0}
          </span>

          <span className="stat-label">
            Matched
          </span>
        </div>


        <div className="summary-stat">
          <span className="stat-number partial-number">
            {summary.partial ?? 0}
          </span>

          <span className="stat-label">
            Partial
          </span>
        </div>


        <div className="summary-stat">
          <span className="stat-number missing-number">
            {summary.missing ?? 0}
          </span>

          <span className="stat-label">
            Missing
          </span>
        </div>


        <div className="summary-stat">
          <span className="stat-number">
            {summary.total_requirements ?? 0}
          </span>

          <span className="stat-label">
            Requirements
          </span>
        </div>

      </div>

    </section>
  );
}

export default MatchSummary;