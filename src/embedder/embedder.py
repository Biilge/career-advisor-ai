from sentence_transformers import SentenceTransformer


class CareerEmbedder:
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2"
    ):
        """
        Initializes the embedding model.

        Args:
            model_name: Name of the SentenceTransformer model.
        """

        print(f"Loading embedding model: {model_name}")

        self.model = SentenceTransformer(model_name)

        print("Embedding model loaded successfully.")

    def embed_documents(self, chunks):
        """
        Converts document chunks into embeddings.
        """

        texts = [
            chunk.page_content
            for chunk in chunks
        ]

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        print(
            f"Created embeddings for "
            f"{len(embeddings)} chunks."
        )

        return embeddings

    def embed_query(self, query: str):
        """
        Converts a user query into an embedding.
        """

        embedding = self.model.encode(
            query,
            convert_to_numpy=True
        )

        return embedding