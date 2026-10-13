from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
import os


DOCUMENTS_FOLDER = "documents"
VECTORSTORE_FOLDER = "vectorstore"


def load_documents():

    documents = []

    for file in os.listdir(DOCUMENTS_FOLDER):

        path = os.path.join(DOCUMENTS_FOLDER, file)

        if file.endswith(".pdf"):

            loader = PyPDFLoader(path)

            docs = loader.load()

            documents.extend(docs)

    return documents


def create_vectorstore():

    print("Loading documents...")

    documents = load_documents()

    print("Documents loaded:", len(documents))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    print("Chunks created:", len(chunks))

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    vectorstore.save_local(VECTORSTORE_FOLDER)

    print("Vector store created successfully!")


if __name__ == "__main__":
    create_vectorstore()