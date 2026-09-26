# JobMatch RAG

An AI-powered resume and job description matching system that uses **Retrieval-Augmented Generation (RAG)** to analyze how a candidate's resume matches the requirements of a job description.

The system extracts resume content, divides it into meaningful sections, generates embeddings, stores the resume knowledge in a vector database, retrieves relevant resume evidence for each job requirement, and uses an LLM to generate evidence-grounded explanations.

---

## Overview

Job seekers often need to manually compare their resume with a job description to understand:

- Which skills match the job
- Which requirements are partially supported
- Which requirements are missing
- What evidence from the resume supports each match
- What areas could be improved

**JobMatch RAG** automates this process using semantic retrieval and LLM-based analysis.

Instead of asking an LLM to analyze the entire resume directly, the system first retrieves relevant resume sections and provides them as evidence to the LLM.

### Basic Flow

```text
Resume PDF
     │
     ▼
Text Extraction
     │
     ▼
Section-Aware Chunking
     │
     ▼
Sentence Transformer Embeddings
     │
     ▼
ChromaDB Vector Database
     │
     │
     │        Job Description
     │               │
     │               ▼
     │       Requirement Extraction
     │               │
     │               ▼
     │       Requirement Embedding
     │               │
     └───────────────┤
                     ▼
             Semantic Retrieval
                     │
                     ▼
              Match Classification
                     │
                     ▼
              Retrieved Evidence
                     │
                     ▼
                 Groq LLM
                     │
                     ▼
             Match Explanation
                     │
                     ▼
               Final Report


## Key Features

- 📄 **Resume PDF Processing**  
  Upload a resume in PDF format and automatically extract its content.

- 🧩 **Section-Aware Resume Chunking**  
  Separates resume content into sections such as Education, Experience, Projects, Technical Skills, and Certifications.

- 🔎 **Semantic Resume Retrieval**  
  Uses Sentence Transformers to retrieve resume evidence that is semantically relevant to each job requirement.

- 🗄️ **Vector Database with ChromaDB**  
  Stores resume embeddings and enables efficient similarity-based retrieval.

- 🎯 **Required & Preferred Requirement Detection**  
  Separates identified job requirements into required and preferred categories.

- 🤝 **Evidence-Based Job Matching**  
  Classifies requirements as **Matched, Partial, or Missing** based on resume evidence.

- 🧠 **RAG-Powered AI Analysis**  
  Uses retrieved resume evidence as context for the LLM instead of sending the entire resume blindly.

- 🛡️ **Grounded LLM Responses**  
  The LLM is instructed to use only the retrieved resume evidence and avoid inventing skills or experience.

- 📊 **Match Summary Dashboard**  
  Displays overall compatibility, matched requirements, partial requirements, and missing requirements.

- 🔬 **Requirement-Level Analysis**  
  Allows users to inspect the evidence, matched terms, evidence type, and AI analysis for individual requirements.

- 💡 **Personalized Improvement Suggestions**  
  Identifies areas where additional project evidence, implementation details, or experience could strengthen the resume.

- 📑 **PDF Report Generation**  
  Generates a downloadable JobMatch RAG report containing the matching results and detailed analysis.

- 💻 **React + FastAPI Architecture**  
  Provides a separate frontend and backend for a clean full-stack architecture.
