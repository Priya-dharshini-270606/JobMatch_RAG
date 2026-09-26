import { useState } from "react";

import Header from "./components/Header.jsx";
import ResumeUpload from "./components/ResumeUpload.jsx";
import JobDescription from "./components/JobDescription.jsx";
import MatchSummary from "./components/MatchSummary.jsx";
import SkillSummary from "./components/SkillSummary.jsx";
import RequirementAnalysis from "./components/RequirementAnalysis.jsx";
import ReportDownload from "./components/ReportDownload.jsx";

import "./App.css";

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");

  const [uploadStatus, setUploadStatus] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const [report, setReport] = useState(null);
  const [error, setError] = useState("");

  const analyzeJob = async () => {
    // =============================
    // VALIDATION
    // =============================
    if (!resumeFile) {
      setError("Please upload your resume PDF.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Please enter the job description.");
      return;
    }

    setError("");
    setReport(null);
    setIsAnalyzing(true);

    try {
      // =============================
      // STEP 1: UPLOAD RESUME
      // =============================
      setUploadStatus("Uploading resume...");

      const formData = new FormData();
      formData.append("file", resumeFile);

      const resumeResponse = await fetch(
        "http://127.0.0.1:8000/upload-resume",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!resumeResponse.ok) {
        const errorText = await resumeResponse.text();

        console.error(
          "Resume upload error:",
          errorText
        );

        throw new Error(
          `Resume upload failed (${resumeResponse.status})`
        );
      }

      const resumeResult =
        await resumeResponse.json();

      console.log(
        "Resume uploaded:",
        resumeResult
      );

      // =============================
      // STEP 2: MATCH JOB DESCRIPTION
      // =============================
      setUploadStatus(
        "Analyzing job description..."
      );

      const matchResponse = await fetch(
        "http://127.0.0.1:8000/match-job",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: jobDescription.trim(),
          }),
        }
      );

      if (!matchResponse.ok) {
        const errorText =
          await matchResponse.text();

        console.error(
          "Match error:",
          errorText
        );

        throw new Error(
          `Job analysis failed (${matchResponse.status})`
        );
      }

      // =============================
      // STEP 3: RECEIVE REPORT
      // =============================
      const result =
        await matchResponse.json();

      console.log(
        "JobMatch Report:",
        result
      );

      setReport(result);

      setUploadStatus(
        "Analysis completed successfully."
      );

    } catch (err) {
      console.error(
        "JobMatch error:",
        err
      );

      setError(
        err.message ||
        "Unable to connect to the JobMatch backend."
      );

      setUploadStatus("");

    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="app">

      <Header />

      <main className="main-container">

        {/* =============================
            HERO SECTION
        ============================== */}
        <section className="hero-section">

          <p className="hero-label">
            AI-POWERED RESUME ANALYSIS
          </p>

          <h1>
            Match Your Resume
            <br />
            With the <span>Right Job</span>
          </h1>

          <p className="hero-description">
            Upload your resume and paste a job
            description to discover matching skills,
            missing requirements, and evidence from
            your resume using RAG-powered analysis.
          </p>

        </section>


        {/* =============================
            INPUT SECTION
        ============================== */}
        <section className="input-grid">

          <ResumeUpload
            resumeFile={resumeFile}
            setResumeFile={setResumeFile}
          />

          <JobDescription
            jobDescription={jobDescription}
            setJobDescription={setJobDescription}
          />

        </section>


        {/* =============================
            STATUS
        ============================== */}
        {uploadStatus && (
          <div className="status-message">
            {uploadStatus}
          </div>
        )}


        {/* =============================
            ERROR
        ============================== */}
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}


        {/* =============================
            ANALYZE BUTTON
        ============================== */}
        <div className="analyze-container">

          <button
            className="analyze-button"
            onClick={analyzeJob}
            disabled={isAnalyzing}
          >
            {isAnalyzing
              ? "Analyzing..."
              : "Analyze Job Match"}
          </button>

        </div>


        {/* =============================
            RESULTS
        ============================== */}
        {report && (

          <section className="results-section">

            {/* =============================
                RESULTS HEADER
            ============================== */}
            <div className="section-heading">

              <p className="section-label">
                ANALYSIS RESULTS
              </p>

              <h2>
                Your JobMatch Report
              </h2>

              <p>
                Resume evidence matched against
                the job requirements.
              </p>

            </div>


            {/* =============================
                OVERALL MATCH
            ============================== */}
            <MatchSummary
              summary={report.overall_summary}
            />


            {/* =============================
                DOWNLOAD FULL REPORT
            ============================== */}
            <div className="download-report-container">

              <ReportDownload
                report={report}
              />

            </div>


            {/* =============================
                REQUIRED / PREFERRED
            ============================== */}
            <div className="category-grid">

              {/* REQUIRED */}
              <div className="category-card">

                <h3>
                  Required Skills
                </h3>

                <div className="category-score">
                  {report.required_summary?.score ?? 0}%
                </div>

                <p>
                  {report.required_summary?.matched ?? 0}
                  {" matched · "}

                  {report.required_summary?.partial ?? 0}
                  {" partial · "}

                  {report.required_summary?.missing ?? 0}
                  {" missing"}
                </p>

              </div>


              {/* PREFERRED */}
              <div className="category-card">

                <h3>
                  Preferred Skills
                </h3>

                <div className="category-score">
                  {report.preferred_summary?.score ?? 0}%
                </div>

                <p>
                  {report.preferred_summary?.matched ?? 0}
                  {" matched · "}

                  {report.preferred_summary?.partial ?? 0}
                  {" partial · "}

                  {report.preferred_summary?.missing ?? 0}
                  {" missing"}
                </p>

              </div>

            </div>


            {/* =============================
                SKILL SUMMARY
            ============================== */}
            <SkillSummary
              skillSummary={report.skill_summary}
            />


            {/* =============================
                RECOMMENDATIONS
            ============================== */}
            {report.recommendations &&
              report.recommendations.length > 0 && (

                <section className="recommendations-section">

                  <div className="section-heading">

                    <p className="section-label">
                      IMPROVEMENTS
                    </p>

                    <h2>
                      Recommendations
                    </h2>

                  </div>

                  <div className="recommendation-list">

                    {report.recommendations.map(
                      (recommendation, index) => (

                        <div
                          className="recommendation-card"
                          key={index}
                        >
                          {recommendation}
                        </div>

                      )
                    )}

                  </div>

                </section>

              )}


            {/* =============================
                REQUIREMENT ANALYSIS
            ============================== */}
            {report.evidence &&
              report.evidence.length > 0 && (

                <RequirementAnalysis
                  evidence={report.evidence}
                />

              )}

          </section>

        )}

      </main>


      {/* =============================
          FOOTER
      ============================== */}
      <footer className="footer">

        <p>
          JobMatch RAG · AI-powered resume
          and job matching
        </p>

      </footer>

    </div>
  );
}

export default App;