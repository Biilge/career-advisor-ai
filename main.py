from src.pipeline.rag_pipeline import CareerRAGPipeline
from src.models.user_profile import UserProfile


def main():

    # Create the user's career profile
    user_profile = UserProfile(
        skills=[
            "Python",
            "SQL",
            "Data Analysis"
        ],
        interests=[
            "Data Science",
            "Artificial Intelligence",
            "Business"
        ],
        education="Computer Science",
        experience_level="Junior",
        preferred_location="Remote"
    )

    # Display the user profile
    print("\nUSER PROFILE")
    print("=" * 80)
    print(user_profile.to_text())

    # Initialize the RAG pipeline
    pipeline = CareerRAGPipeline(
        index_path="data/processed/faiss_index.index",
        metadata_path="data/processed/chunks_metadata.json",
        model_name="qwen2.5-0.5b"
    )

    # Get career recommendations based on the user profile
    response = pipeline.ask(
        user_profile=user_profile,
        top_k=5
    )

    print("\n" + "=" * 80)
    print("CAREER ADVISOR RESPONSE")
    print("=" * 80 + "\n")

    print(response)

    # Unload the local model
    pipeline.close()


if __name__ == "__main__":
    main()