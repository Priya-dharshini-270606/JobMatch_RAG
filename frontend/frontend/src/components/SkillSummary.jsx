function SkillSummary({ skillSummary }) {
  if (!skillSummary) {
    return null;
  }

  const matched = skillSummary.matched || [];
  const partial = skillSummary.partial || [];
  const missing = skillSummary.missing || [];

  return (
    <section className="skill-summary-section">

      <div className="section-heading">
        <p className="section-label">SKILL BREAKDOWN</p>
        <h2>Skills Analysis</h2>
      </div>

      <div className="skill-summary-grid">

        <div className="skill-group">
          <h3>Matched</h3>

          <div className="skill-pills">
            {matched.length > 0 ? (
              matched.map((skill, index) => (
                <span className="skill-pill matched" key={index}>
                  {skill}
                </span>
              ))
            ) : (
              <p>No matched skills.</p>
            )}
          </div>
        </div>

        <div className="skill-group">
          <h3>Partial</h3>

          <div className="skill-pills">
            {partial.length > 0 ? (
              partial.map((skill, index) => (
                <span className="skill-pill partial" key={index}>
                  {skill}
                </span>
              ))
            ) : (
              <p>No partial skills.</p>
            )}
          </div>
        </div>

        <div className="skill-group">
          <h3>Missing</h3>

          <div className="skill-pills">
            {missing.length > 0 ? (
              missing.map((skill, index) => (
                <span className="skill-pill missing" key={index}>
                  {skill}
                </span>
              ))
            ) : (
              <p>No missing skills.</p>
            )}
          </div>
        </div>

      </div>

    </section>
  );
}

export default SkillSummary;