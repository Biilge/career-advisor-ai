from src.generator.generator import CareerGenerator


def main():

    generator = CareerGenerator(
        model_name="qwen2.5-0.5b"
    )

    response = generator.generate(
        query=(
            "I have experience with Python, SQL, "
            "and data analysis. "
            "What career paths should I consider?"
        ),
        retrieved_context=(
            "Relevant job information mentions experience "
            "with Python, SQL, databases, data analytics, "
            "statistical analysis, and data mining."
        )
    )

    print("\nCareer Recommendation:\n")
    print(response)

    generator.unload()


if __name__ == "__main__":
    main()