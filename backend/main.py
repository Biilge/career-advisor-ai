from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.models.user_profile import UserProfile
from src.pipeline.rag_pipeline import CareerRAGPipeline


app = FastAPI(
    title="Career Advisor AI",
    description="Local AI career recommendation API",
    version="1.0.0"
)


# Allow requests from the local frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CareerProfileRequest(BaseModel):
    skills: list[str]
    interests: list[str]
    education: str
    experience_level: str
    preferred_location: str


class ChatRequest(BaseModel):
    skills: list[str]
    interests: list[str]
    education: str
    experience_level: str
    preferred_location: str
    message: str


pipeline = None


def get_pipeline():
    global pipeline

    if pipeline is None:
        pipeline = CareerRAGPipeline(
            index_path="data/processed/faiss_index.index",
            metadata_path="data/processed/chunks_metadata.json",
            model_name="qwen2.5-0.5b"
        )

    return pipeline


@app.get("/")
def root():
    return {
        "message": "Career Advisor AI API is running."
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/recommend")
def recommend(profile: CareerProfileRequest):

    user_profile = UserProfile(
        skills=profile.skills,
        interests=profile.interests,
        education=profile.education,
        experience_level=profile.experience_level,
        preferred_location=profile.preferred_location
    )

    career_pipeline = get_pipeline()

    response = career_pipeline.ask(
        user_profile=user_profile,
        top_k=5
    )

    return {
        "success": True,
        "recommendations": response
    }


@app.post("/chat")
def chat(request: ChatRequest):

    user_profile = UserProfile(
        skills=request.skills,
        interests=request.interests,
        education=request.education,
        experience_level=request.experience_level,
        preferred_location=request.preferred_location
    )

    career_pipeline = get_pipeline()

    response = career_pipeline.chat(
        user_profile=user_profile,
        user_message=request.message,
        top_k=5
    )

    return {
        "success": True,
        "message": response
    }