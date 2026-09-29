from pathlib import Path
import json

import faiss


class FAISSStore:
    def __init__(self):
        """
        Initializes an empty FAISS vector store.
        """

        self.index = None
        self.metadata = []

    def build_index(self, embeddings):
        """
        Creates a FAISS index from document embeddings.
        """

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(
            embeddings.astype("float32")
        )

        print(
            f"FAISS index created with "
            f"{self.index.ntotal} vectors."
        )

    def set_metadata(self, chunks):
        """
        Stores each chunk together with its original
        job metadata.
        """

        self.metadata = []

        for index, chunk in enumerate(chunks):

            chunk_metadata = {
                "chunk_id": index,
                "job_id": chunk.metadata.get("job_id"),
                "company": chunk.metadata.get("company"),
                "title": chunk.metadata.get("title"),
                "category": chunk.metadata.get("category"),
                "location": chunk.metadata.get("location"),
                "text": chunk.page_content
            }

            self.metadata.append(
                chunk_metadata
            )

        print(
            f"Metadata created for "
            f"{len(self.metadata)} chunks."
        )

    def save(self, index_path: str, metadata_path: str):
        """
        Saves the FAISS index and metadata to disk.
        """

        if self.index is None:
            raise ValueError(
                "FAISS index has not been created yet."
            )

        Path(index_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        Path(metadata_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            index_path
        )

        with open(
            metadata_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.metadata,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            "FAISS index and metadata saved successfully."
        )

    def load(self, index_path: str, metadata_path: str):
        """
        Loads a FAISS index and metadata from disk.
        """

        self.index = faiss.read_index(
            index_path
        )

        with open(
            metadata_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.metadata = json.load(file)

        print(
            f"FAISS index loaded with "
            f"{self.index.ntotal} vectors."
        )

        print(
            f"Loaded metadata for "
            f"{len(self.metadata)} chunks."
        )