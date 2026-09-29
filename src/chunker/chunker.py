from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class CareerChunker:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 80
    ):
        """
        Initializes the text splitter.
        """

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )

    def create_career_documents(self, dataframe):
        """
        Converts each job record into a Document object
        with structured metadata.
        """

        documents = []

        for job_id, (_, row) in enumerate(
            dataframe.iterrows()
        ):

            document_text = f"""
Company: {row['Company']}

Job Title: {row['Title']}

Category: {row['Category']}

Location: {row['Location']}

Responsibilities:
{row['Responsibilities']}

Minimum Qualifications:
{row['Minimum Qualifications']}

Preferred Qualifications:
{row['Preferred Qualifications']}
"""

            metadata = {
                "job_id": job_id,
                "company": str(row["Company"]),
                "title": str(row["Title"]),
                "category": str(row["Category"]),
                "location": str(row["Location"])
            }

            document = Document(
                page_content=document_text.strip(),
                metadata=metadata
            )

            documents.append(document)

        print(
            f"Created {len(documents)} career documents."
        )

        return documents

    def chunk_documents(self, documents):
        """
        Splits career documents into smaller chunks while
        preserving the metadata of the original job record.
        """

        chunks = self.text_splitter.split_documents(
            documents
        )

        print(
            f"Created {len(chunks)} chunks."
        )

        return chunks