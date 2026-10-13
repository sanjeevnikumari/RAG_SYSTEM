# 📚 Local AI Document Assistant — RAG with Ollama

Ask questions about your documents using a locally running large language model. This project implements **Retrieval-Augmented Generation (RAG)** with **Ollama**, **LangChain**, **FAISS**, and **Streamlit**.

The application retrieves relevant passages from your own documents and supplies them as context to the language model, helping it answer document-specific questions without sending your documents to a hosted LLM API.

> **Status:** Starter implementation. The core workflow supports PDF ingestion, semantic retrieval, and question answering. Features such as document upload, persistent chat history, hybrid search, and reranking can be added as future improvements.

## ✨ Features

- **Local LLM inference** with Ollama (`llama3.2:3b` by default).
- **Local embeddings** with `nomic-embed-text`.
- **PDF processing** with PyPDF.
- **Text chunking** with LangChain's `RecursiveCharacterTextSplitter`.
- **Semantic search** using a FAISS vector index.
- **Context-grounded answers** using retrieved document chunks.
- **Streamlit interface** for asking questions.
- **Source metadata** such as document path and page number (depending on the loader and UI implementation).

## 🧠 How RAG works

RAG has two main stages:

### 1. Indexing (run when documents change)

```text
PDF files
   ↓
Text extraction
   ↓
Chunking with overlap
   ↓
Embedding model (nomic-embed-text)
   ↓
FAISS vector index
```

### 2. Question answering

```text
User question
   ↓
Question embedding
   ↓
FAISS retrieves the most relevant chunks
   ↓
Retrieved context + question
   ↓
Ollama LLM (llama3.2:3b)
   ↓
Answer
```

The embedding model converts text into numerical vectors for similarity search. The LLM generates the response; it does not create the vector index.

## 🧰 Tech stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Ollama | Runs local models |
| Llama 3.2 3B | Answer generation |
| Nomic Embed Text | Text embeddings |
| LangChain | Document, splitter, model, and retriever integrations |
| FAISS | Local vector similarity search |
| PyPDF | PDF text extraction |
| Streamlit | Web UI |

## 📁 Project structure

For the starter implementation described here:

```text
ollama-rag/
├── app.py                 # Streamlit interface
├── ingest.py              # Loads PDFs, chunks text, builds FAISS index
├── rag.py                 # Retrieval and answer generation
├── requirements.txt       # Python dependencies
├── documents/             # Add your source PDFs here
└── vectorstore/            # Generated FAISS index (created during ingestion)
```

If your code uses a modular `ingestion/`, `retrieval/`, and `generation/` layout instead, update this tree to match your actual repository.

## ⚙️ Prerequisites

- Windows, macOS, or Linux
- Python 3.10+ recommended
- [Ollama](https://ollama.com/download) installed
- Enough RAM and disk space for the selected local models
- Internet access for the initial model downloads and Python package installation

## 🚀 Getting started

### 1. Clone the repository

Replace the placeholder URL with your GitHub repository URL.

```bash
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
```

### 2. Create and activate a virtual environment

**Windows — PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```bat
venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Example `requirements.txt` for the starter code:

```text
streamlit
langchain
langchain-community
langchain-ollama
langchain-text-splitters
faiss-cpu
pypdf
python-docx
```

Keep this file aligned with the imports used in your repository. `python-docx` is only needed if you implement DOCX ingestion.

### 4. Download the Ollama models

Open a terminal and run:

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

Check that both are installed:

```bash
ollama list
```

Test the language model:

```bash
ollama run llama3.2:3b
```

Type a question, then use `/bye` to exit. Ollama normally runs its local service in the background after installation. If a connection error occurs, start Ollama from the application or run `ollama serve` in a separate terminal if needed.

### 5. Add your documents

Create a `documents` directory beside `app.py` and `ingest.py`, then place your PDFs inside it:

```text
documents/
├── machine_learning.pdf
└── course_notes.pdf
```

Use documents you have permission to process. Scanned PDFs may need OCR because basic PDF text extraction cannot reliably read text stored only as page images.

### 6. Build the vector index

Run this from the project root:

```bash
python ingest.py
```

The script should load the PDFs, split their text into chunks, create embeddings, and save the FAISS index to `vectorstore/`.

Run ingestion again when you add or change documents, unless your implementation automatically updates the index.

### 7. Ask questions in the terminal (optional)

If `rag.py` includes a command-line entry point:

```bash
python rag.py
```

Ask a question that can be answered from the indexed documents. The script should retrieve relevant chunks and pass them to Ollama to generate an answer.

### 8. Launch the Streamlit application

```bash
streamlit run app.py
```

Open the local URL printed in the terminal, usually `http://localhost:8501`.

> **First-run note:** The first response can take longer while the model loads. Retrieval will only work after a vector index has been created and the configured embedding model is available.

## 🔧 Configuration

The starter implementation commonly uses:

| Setting | Default | Meaning |
|---|---|---|
| LLM model | `llama3.2:3b` | Generates answers |
| Embedding model | `nomic-embed-text` | Embeds documents and questions |
| Chunk size | `500` characters | Approximate maximum chunk length |
| Chunk overlap | `50` characters | Shared text between adjacent chunks |
| Top-k | `4` | Number of chunks retrieved per question |

If these values are defined in `config.py`, update them there. Otherwise, edit the corresponding values in your code. Chunk size and overlap are starting points—not universal best settings—and should be evaluated on your documents.

## 🛡️ Privacy and limitations

- Model inference and vector search run locally when using the local Ollama service and local FAISS index.
- Initial installation and model downloads require internet access.
- Local processing does not automatically make every component secure; protect your computer, files, and local services.
- RAG can still return incorrect or incomplete answers. Retrieved context and citations should be checked.
- A prompt telling the model to use only the context reduces unsupported answers but does **not** guarantee that hallucinations never occur.
- Treat text inside documents as untrusted input. Do not let document instructions override application rules.
- FAISS indexes created with LangChain may include a pickle file. Only load indexes you created or otherwise trust. `allow_dangerous_deserialization=True` can execute malicious pickle content if the file is untrusted.
- PDF files with scanned pages may require an OCR stage.
- Large models and large documents need more RAM, storage, and processing time.

## 🧪 Troubleshooting

### `ollama` is not recognized

Install Ollama, restart the terminal, and check:

```bash
ollama --version
```

### Cannot connect to Ollama

Make sure the Ollama application/service is running. Test:

```bash
ollama list
```

If necessary, run `ollama serve` in a separate terminal, provided no Ollama server is already running on the default port.

### Model not found

Pull the exact model name configured in the project:

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

### Vector store not found

Run ingestion from the project root:

```bash
python ingest.py
```

Confirm that the `vectorstore/` directory was created in the path expected by `rag.py`.

### No useful answer is returned

- Confirm that the source PDF contains extractable text.
- Ask a specific question answered in the document.
- Inspect the retrieved chunks before changing the prompt.
- Try adjusting chunk size, overlap, or `TOP_K`.
- Verify that the same embedding model is used to build and query the index.

### Python import or dependency errors

Activate the correct virtual environment and install dependencies again:

```bash
python -m pip install -r requirements.txt
```

If package versions conflict, use a clean virtual environment and pin tested versions once the project works.

## 🗺️ Roadmap

- [ ] Upload PDF, TXT, and DOCX files through Streamlit
- [ ] Display source passages and page-level citations
- [ ] Add chat history and contextual follow-up questions
- [ ] Add metadata filters and document selection
- [ ] Add hybrid retrieval (vector + keyword search)
- [ ] Add reranking
- [ ] Add automated ingestion/re-indexing and duplicate handling
- [ ] Evaluate retrieval and answer quality with a small test set
- [ ] Add tests, logging, and clearer error messages
- [ ] Add Docker support (optional)

## 📌 Future improvements

A strong RAG system should be evaluated, not judged only by whether it produces fluent answers. Test it with questions whose answers are present in the documents, questions whose answers are absent, and follow-up questions. Track retrieval relevance, answer correctness, source support, latency, and failure cases.

## 🤝 Contributing

Contributions and suggestions are welcome. For substantial changes, open an issue first to discuss the proposed improvement.

## 📄 License

Choose a license before publishing this repository. If you intend to use an open-source license, add the corresponding `LICENSE` file (for example, MIT) and update this section accordingly.
<img width="1920" height="1080" alt="Screenshot (782)" src="https://github.com/user-attachments/assets/7fb72e70-ad8a-4cba-a794-f3e581935889" />

---

**Built with Python, Ollama, LangChain, FAISS, and Streamlit.**
