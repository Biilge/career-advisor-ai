from src.embedder.embedder import CareerEmbedder
from src.store.faiss_store import FAISSStore
from src.retriever.retriever import CareerRetriever
from src.generator.generator import CareerGenerator
from src.models.user_profile import UserProfile


class CareerRAGPipeline:

    def __init__(
        self,
        index_path: str,
        metadata_path: str,
        model_name: str = "qwen2.5-0.5b"
    ):
        print("Initializing Career Advisor RAG Pipeline...\n")

        self.embedder = CareerEmbedder()

        self.store = FAISSStore()

        self.store.load(
            index_path=index_path,
            metadata_path=metadata_path
        )

        self.retriever = CareerRetriever(
            store=self.store,
            embedder=self.embedder
        )

        self.generator = CareerGenerator(
            model_name=model_name
        )

        print("\nCareer Advisor RAG Pipeline is ready.")

    def ask(
        self,
        user_profile: UserProfile,
        top_k: int = 5
    ) -> str:

        # 1. Create optimized retrieval query
        retrieval_query = (
            user_profile.to_retrieval_query()
        )

        # 2. Retrieve job information
        results = self.retriever.retrieve(
            query=retrieval_query,
            top_k=top_k
        )

        # 3. Remove duplicate job titles
        unique_results = []
        seen_titles = set()

        for result in results:

            title = result.get("title")

            if title and title not in seen_titles:

                unique_results.append(result)
                seen_titles.add(title)

        # 4. Allowed titles
        allowed_job_titles = [
            result["title"]
            for result in unique_results
        ]

        # 5. Build context
        context_parts = []

        for i, result in enumerate(
            unique_results,
            start=1
        ):

            context = f"""
SOURCE {i}

Job Title: {result.get('title', 'Unknown')}
Company: {result.get('company', 'Unknown')}
Category: {result.get('category', 'Unknown')}
Location: {result.get('location', 'Unknown')}

Job Information:
{result.get('text', '')}
"""

            context_parts.append(
                context.strip()
            )

        retrieved_context = "\n\n".join(
            context_parts
        )

        # 6. Let the local model select titles
        model_output = self.generator.generate(
            user_profile=user_profile.to_text(),
            retrieved_context=retrieved_context,
            allowed_job_titles=allowed_job_titles
        )

        # 7. Validate model output
        selected_titles = []

        for line in model_output.splitlines():

            cleaned_line = line.strip()

            cleaned_line = cleaned_line.lstrip(
                "-•0123456789. "
            )

            for title in allowed_job_titles:

                if (
                    title.lower()
                    in cleaned_line.lower()
                    and title not in selected_titles
                ):
                    selected_titles.append(title)

        # 8. Fallback if model output is invalid
        if len(selected_titles) < 2:

            selected_titles = allowed_job_titles[:4]

        else:

            selected_titles = selected_titles[:4]

        # 9. Build deterministic response
        response_parts = []

        for index, title in enumerate(
            selected_titles,
            start=1
        ):

            job = next(
                result
                for result in unique_results
                if result["title"] == title
            )

            response_parts.append(
                f"{index}. {title}\n"
                f"   Company: {job.get('company', 'Unknown')}\n"
                f"   Category: {job.get('category', 'Unknown')}\n"
                f"   Location: {job.get('location', 'Unknown')}\n"
                f"   Relevant information: "
                f"{job.get('text', '').replace(chr(10), ' ')[:350]}"
            )

        return "\n\n".join(response_parts)

    def chat(
        self,
        user_profile: UserProfile,
        user_message: str,
        top_k: int = 5
    ) -> str:
        """
        Answers a career-related user question using
        retrieved job information and the local model.
        """

        # 1. Retrieve relevant job information
        results = self.retriever.retrieve(
            query=user_message,
            top_k=top_k
        )

        # 2. Build context for the local model
        context_parts = []

        for i, result in enumerate(
            results,
            start=1
        ):

            context = f"""
SOURCE {i}

Job Title: {result.get('title', 'Unknown')}
Company: {result.get('company', 'Unknown')}
Category: {result.get('category', 'Unknown')}
Location: {result.get('location', 'Unknown')}

Job Information:
{result.get('text', '')}
"""

            context_parts.append(
                context.strip()
            )

        retrieved_context = "\n\n".join(
            context_parts
        )

        # 3. Generate the answer with the local model
        response = self.generator.chat(
            user_profile=user_profile.to_text(),
            retrieved_context=retrieved_context,
            user_message=user_message
        )

        return response

    def close(self):

        self.generator.unload()