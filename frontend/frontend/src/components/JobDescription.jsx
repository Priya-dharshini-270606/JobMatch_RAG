function JobDescription({ jobDescription = "", setJobDescription }) {
  return (
    <div className="input-card">

      <div className="input-card-header">
        <div>
          <p className="input-label">JOB DESCRIPTION</p>
          <h2>Paste Job Description</h2>
        </div>

        <span className="input-number">02</span>
      </div>

      <textarea
        className="job-description-input"
        value={jobDescription}
        onChange={(event) => setJobDescription(event.target.value)}
        placeholder="Paste the complete job description here..."
        rows={12}
      />

      <div className="character-count">
        {jobDescription.length} characters
      </div>

    </div>
  );
}

export default JobDescription;