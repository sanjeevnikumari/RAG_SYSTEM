from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS


VECTORSTORE_FOLDER = "vectorstore"


def load_vectorstore():

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    vectorstore = FAISS.load_local(
        VECTORSTORE_FOLDER,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def ask_question(question):

    vectorstore = load_vectorstore()

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 4
        }
    )

    documents = retriever.invoke(question)

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
You are a helpful document assistant.

Answer the question using ONLY the context provided below.

If the answer is not present in the context,
say "I could not find this information in the documents."

Context:
{context}

Question:
{question}

Answer:
"""

    llm = OllamaLLM(
        model="llama3.2:3b"
    )

    answer = llm.invoke(prompt)

    return answer


if __name__ == "__main__":

    question = input("Ask a question: ")

    answer = ask_question(question)

    print("\nAnswer:")
    print(answer)