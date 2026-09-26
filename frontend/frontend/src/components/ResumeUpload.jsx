function ResumeUpload({ resumeFile, setResumeFile }) {
  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    if (file.type !== "application/pdf") {
      alert("Please select a PDF file.");
      event.target.value = "";
      return;
    }

    setResumeFile(file);
  };

  return (
    <div className="input-card">

      <div className="input-card-header">
        <div>
          <p className="input-label">RESUME</p>
          <h2>Upload your Resume</h2>
        </div>

        <span className="input-number">01</span>
      </div>

      <div className="upload-area">

        <input
          id="resume-upload"
          type="file"
          accept=".pdf,application/pdf"
          onChange={handleFileChange}
          className="resume-file-input"
        />

        <label
          htmlFor="resume-upload"
          className="upload-content"
        >
          <div className="upload-icon">
            ↑
          </div>

          {resumeFile ? (
            <>
              <div className="upload-title">
                Resume selected
              </div>

              <div className="selected-file">
                {resumeFile.name}
              </div>

              <div className="upload-subtitle">
                Click here to change the file
              </div>
            </>
          ) : (
            <>
              <div className="upload-title">
                Click to upload your resume
              </div>

              <div className="upload-subtitle">
                PDF files only · Maximum 10 MB
              </div>
            </>
          )}
        </label>

      </div>

    </div>
  );
}

export default ResumeUpload;