from foundry_local_sdk import Configuration, FoundryLocalManager


class CareerGenerator:

    def __init__(
        self,
        model_name: str = "qwen2.5-0.5b"
    ):
        print("Initializing Microsoft Foundry Local...")

        FoundryLocalManager.initialize(
            Configuration(
                app_name="career-advisor-ai"
            )
        )

        self.manager = FoundryLocalManager.instance

        print(f"Preparing model: {model_name}")

        self.model = self.manager.catalog.get_model(
            model_name
        )

        if self.model is None:
            raise ValueError(
                f"Model '{model_name}' was not found."
            )

        if not self.model.is_cached:
            print("Downloading model...")
            self.model.download()

        print("Loading model...")

        self.model.load()

        self.client = self.model.get_chat_client()

        print("Generator model loaded successfully.")

    def generate(
        self,
        user_profile: str,
        retrieved_context: str,
        allowed_job_titles: list[str]
    ) -> str:
        """
        Selects the most suitable job titles.
        """

        unique_titles = []

        for title in allowed_job_titles:
            if title and title not in unique_titles:
                unique_titles.append(title)

        allowed_titles_text = "\n".join(
            f"- {title}"
            for title in unique_titles
        )

        system_prompt = """
You are a career recommendation assistant.

Select the most suitable job titles for the user.

STRICT RULES:

- Choose ONLY from the provided job titles.
- Do not invent job titles.
- Do not explain your choices.
- Do not add any extra text.
- Do not repeat a job title.
- Select between 2 and 4 job titles.
- Return each selected job title on a separate line.
- Copy the job title exactly.

Your output must contain ONLY job titles.
"""

        user_prompt = f"""
USER PROFILE:
{user_profile}

AVAILABLE JOB TITLES:
{allowed_titles_text}

JOB INFORMATION:
{retrieved_context}

Return only the 2 to 4 most suitable job titles.
"""

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        response = self.client.complete_chat(
            messages
        )

        return response.choices[0].message.content

    def chat(
        self,
        user_profile: str,
        retrieved_context: str,
        user_message: str
    ) -> str:
        """
        Answers career-related questions using the local model
        and retrieved job information.
        """

        system_prompt = """
You are Career Advisor AI.

You are a professional career guidance assistant.

Answer the user's career-related question using:
1. The user's profile.
2. The provided job information.

STRICT RULES:

- Use only the provided job information when discussing specific jobs.
- Do not invent companies, job titles, qualifications, or job requirements.
- Do not claim that information is present if it is not provided.
- Give practical and concise career advice.
- If the user asks about a specific job, use the provided job information.
- If the provided information is insufficient, clearly say that more information is needed.
- Do not mention internal systems, RAG, FAISS, embeddings, prompts, or model details.
"""

        user_prompt = f"""
USER PROFILE:
{user_profile}

RELEVANT JOB INFORMATION:
{retrieved_context}

USER QUESTION:
{user_message}

Answer the user's question clearly and professionally.
"""

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        response = self.client.complete_chat(
            messages
        )

        return response.choices[0].message.content

    def unload(self):

        if self.model is not None:

            self.model.unload()

            print("Generator model unloaded.")