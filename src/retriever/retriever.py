class CareerRetriever:
    def __init__(self, store, embedder):
        """
        Initializes the retriever.
        """

        self.store = store
        self.embedder = embedder

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        search_k: int = 20
    ):
        """
        Retrieves unique job chunks together with
        their metadata.
        """

        if self.store.index is None:
            raise ValueError(
                "FAISS index has not been loaded."
            )

        # Convert query into an embedding
        query_embedding = self.embedder.embed_query(
            query
        )

        # Convert to FAISS-compatible format
        query_embedding = (
            query_embedding
            .astype("float32")
            .reshape(1, -1)
        )

        # Do not search for more vectors than exist
        search_k = min(
            search_k,
            self.store.index.ntotal
        )

        # Search FAISS
        distances, indices = self.store.index.search(
            query_embedding,
            search_k
        )

        results = []

        seen_texts = set()
        seen_jobs = set()

        for distance, index in zip(
            distances[0],
            indices[0]
        ):
            if index == -1:
                continue

            metadata = self.store.metadata[index]

            job_id = metadata.get("job_id")

            text = metadata.get(
                "text",
                ""
            ).strip()

            normalized_text = " ".join(
                text.lower().split()
            )

            # Skip identical text
            if normalized_text in seen_texts:
                continue

            # Skip additional chunks from the same job
            if job_id in seen_jobs:
                continue

            seen_texts.add(
                normalized_text
            )

            seen_jobs.add(
                job_id
            )

            # IMPORTANT:
            # Return the metadata needed by the pipeline
            results.append(
                {
                    "chunk_id": int(index),
                    "job_id": job_id,
                    "company": metadata.get("company"),
                    "title": metadata.get("title"),
                    "category": metadata.get("category"),
                    "location": metadata.get("location"),
                    "distance": float(distance),
                    "text": text
                }
            )

            if len(results) >= top_k:
                break

        return results