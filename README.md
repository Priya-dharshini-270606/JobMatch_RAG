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
