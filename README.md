# Career Advisor AI

An AI-powered career recommendation and career guidance system built with a local RAG pipeline.

Career Advisor AI analyzes a user's skills, interests, education, experience level, and preferred location to recommend relevant career opportunities from a job dataset.

## Features

- Personalized career recommendations
- AI-powered career advisor chatbot
- Retrieval-Augmented Generation (RAG)
- Local and offline AI inference
- Semantic search with FAISS
- Custom web interface

## Technologies

- Python
- FastAPI
- FAISS
- Sentence Transformers
- `all-MiniLM-L6-v2`
- Microsoft Foundry Local
- Qwen 2.5 0.5B
- HTML, CSS & JavaScript

## Architecture

```text
Job Dataset
    ↓
Loader
    ↓
Chunker
    ↓
Embeddings
    ↓
FAISS Vector Store
    ↓
Retriever
    ↓
Local LLM
    ↓
Career Recommendations
AI-Assisted Development

This project was developed with the assistance of AI tools for architecture, coding, debugging, prompt engineering, and documentation.

The application itself uses Qwen 2.5 0.5B locally through Microsoft Foundry Local.

Local & Offline

The application is designed to run locally without relying on cloud-based AI APIs after the required models and dependencies are installed.

Project Structure
career-advisor-ai/
├── backend/
├── data/
├── frontend/
├── src/
├── main.py
├── requirements.txt
└── test_generator.py
