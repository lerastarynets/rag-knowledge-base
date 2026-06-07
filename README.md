# RAG Knowledge Base — Personal AI Research Assistant

> Ask questions in plain English. Get grounded answers streamed in real time, with inline source citations woven into the response text.

---

## What this project does

This is a full-stack AI application that lets you upload documents — PDFs, Word files, web pages, YouTube videos — and then have a conversation with them. You ask a question, the system finds the most relevant pieces of your documents, passes them to an LLM, and streams back a grounded answer. Source references appear inline in the answer text using bracketed citation headers (for example, `[filename, page 47]`).

If the system cannot find a confident answer in your documents, it tells you that instead of making something up.

---

## The problem it solves

Imagine you have dozens of PDFs from TransUnion, Experian, and FICO covering credit scoring models, bureau data dictionaries, and integration specs. You need to answer a question like:

> *"What attributes does TransUnion expose for thin-file applicants, and how do they compare to Experian's equivalent fields?"*

Without this tool: you open four PDFs, ctrl+F through them for 20 minutes, manually cross-reference sections, hope you didn't miss anything.

With this tool: you type the question, hit enter, and in a few seconds you get a structured answer with inline citations such as `[TransUnion_DataDictionary_v3.pdf, page 47]` and `[Experian_PowerCurve_Guide.pdf, page 12]`.

---

## Why I built this — credit risk & bureau data

I work with **credit risk and decisioning** documentation: long PDFs from bureau and score providers, dense attribute dictionaries, and integration specs that cross-reference each other constantly. Questions like *"How does TransUnion define thin-file attributes compared to Experian?"* require pulling exact field names and thresholds from multiple sources — work that does not map well to keyword search or a general-purpose chatbot.

**RAG fits this problem** because answers must stay tied to documents I actually uploaded: retrieve the right chunks, cite the source page, and refuse to answer when the evidence is not there. That is the core loop this project implements.

The domain focus is reflected in the **system prompt** (`chain/prompts.py`), which frames the assistant around credit risk, bureau data, and providers such as TransUnion, Experian, and FICO — not in bundled corpus files or ingest logic. You bring your own documents; the app is source-type agnostic (PDF, DOCX, URL, YouTube).

Typical corpus I had in mind when designing and testing it:

- **TransUnion** — CreditVision data dictionaries, attribute catalogues, API integration docs
- **Experian** — PowerCurve documentation, Mosaic segmentation guides, bureau data specs
- **FICO** — Score explainability guides, scorecard development methodology

**What this project covers, and why each piece matters for that use case:**

| Area | What the project does | Why it matters here |
|---|---|---|
| Chunking | Recursive character splitting (2000 chars, 200 overlap) | Bureau PDFs are long; overlap keeps attribute definitions from being cut in half at page boundaries |
| Embeddings + vector search | `text-embedding-3-small` stored in Qdrant | Semantic lookup across differently worded specs ("thin file" vs "limited credit history") |
| Two-stage retrieval | Top 20 vector hits → Cohere rerank to top 5 | Reduces noise when many chunks mention similar scoring terms |
| Relevance guardrail | Top rerank score must be ≥ 0.3 | Stops the model from speculating when nothing in the corpus actually matches |
| Grounded generation | Context injected with citation headers; temperature 0 | Forces exact attribute names, score ranges, and page-level citations |
| Streaming chat | Plain-text stream over `POST /chat/` | Usable for long, multi-source answers without waiting for the full response |
| LangSmith feedback | Thumbs up/down on each run | Trace quality on real bureau-style questions over time |

The stack is general-purpose — swap in any document set and the pipeline stays the same. I chose credit risk as the design anchor because it demands precision, cross-document synthesis, and a hard refusal when the corpus does not support an answer.

---

## How it works, step by step

### Step 1 — You upload a document

You upload a PDF or Word file via the sidebar file picker. Locally, you can also paste a web page or YouTube URL — the backend routes the request to the matching ingestor (PDF, DOCX, URL, or YouTube). URL and YouTube ingestion is disabled on hosted deployments (see [Deployment notes](#deployment-notes)).

### Step 2 — Ingestion pipeline

The ingestor loads raw text from the source, then splits it with LangChain's `RecursiveCharacterTextSplitter` — **2000 characters per chunk, 200 characters overlap** (character-based, not token-based). Each chunk keeps metadata such as source filename, page number (PDFs), `source_type`, and title/author where available.

Each chunk is embedded with **OpenAI `text-embedding-3-small`** (1536-dimensional vectors) and stored in **Qdrant**. Ingestion is **synchronous**: indexing finishes before the API returns `{ status: "ok" }`.

### Step 3 — You ask a question

You type a question in the chat textarea and press Enter. The frontend sends `POST /chat/` with your message and a client-generated `session_id` (reserved for future multi-turn memory; not used server-side yet).

### Step 4 — Retrieval

Your question is embedded with the same model. Qdrant returns the **top 20** nearest chunks via vector similarity search. A **Cohere `rerank-english-v3.0`** cross-encoder re-scores those candidates and keeps the **top 5**, attaching a `relevance_score` to each result.

### Step 5 — Hallucination guardrail

Before generation, the backend checks the **top reranker score**. If no documents were retrieved, the score is missing, or it falls **below 0.3**, the chain stops and the API streams a fixed fallback message instead of calling the LLM:

> *"I could not find a confident answer to your question in the provided documents."*

### Step 6 — Answer generation with streaming

The surviving chunks are formatted with citation headers prepended to each one (for example, `[filename, page 47]` or `[Article: domain — page title]`) and injected into a LangChain prompt. **OpenAI `gpt-5.4-mini`** (temperature 0) generates the answer strictly from that context.

The response streams back as **plain text** over `POST /chat/` (`StreamingResponse`, not SSE). The frontend reads the body with the Fetch API and `ReadableStream`, appending tokens to the message bubble as they arrive.

### Step 7 — Citations

Citations are **inline in the answer text**. The system prompt instructs the model to reproduce the bracketed citation headers exactly as they appear in the retrieved context. Formats include `[filename, page N]`, `[Article: domain — title]`, and `[Video: "title" by author]`.

### Step 8 — Feedback

After each chat response, the backend creates **LangSmith presigned feedback tokens** for the run and returns them in the `X-Feedback-Up` and `X-Feedback-Down` response headers. Thumbs up/down buttons in the UI POST directly to those LangSmith URLs (there is no `/feedback` backend route). Feedback is recorded on the LangSmith trace for that chat run.

---

## Architecture overview

```
┌──────────────────────────────────────────────────────────┐
│                     Next.js Frontend                      │
│  Sidebar (file + URL ingest)  │  Chat (useStreamingChat)   │
│                               │  Thumbs up/down → LangSmith │
└──────────────┬────────────────────────────┬──────────────┘
               │ REST + plain-text stream    │ presigned POST
┌──────────────▼────────────────────────────▼──────────────┐
│                     FastAPI Backend                       │
│            /ingest/file   /ingest/url   /chat             │
└──────┬──────────────────────────────┬─────────────────────┘
       │                              │
┌──────▼──────────┐          ┌────────▼─────────────────────┐
│    Ingestor     │          │   LangChain RAG chain         │
│  PDF · DOCX     │          │  Search (k=20) → Rerank (top 5)│
│  URL · YouTube  │          │  → Guardrail → Prompt → LLM   │
└──────┬──────────┘          │  → StreamingResponse (text)   │
       │ embed + store       └────────┬─────────────────────┘
       └──────────────────────────────►│      Qdrant          │
                                       │   (vector store)     │
                                       └──────────────────────┘
```

---

## Tech stack

| Layer | Technology | Why |
|---|---|---|
| Frontend | Next.js 14, TypeScript | App router, client components |
| Chat UI | Custom streaming hook (`useStreamingChat`) | Fetch + `ReadableStream`, no extra chat framework |
| Styling | Tailwind + shadcn/ui | Fast, clean, dark theme |
| Backend | FastAPI, Python 3.11 | Async, great for streaming responses |
| AI orchestration | LangChain | Runnable chain for retrieval + generation |
| Embeddings | OpenAI `text-embedding-3-small` | 1536-dim vectors, good price/quality |
| LLM | OpenAI `gpt-5.4-mini` | Hardcoded in `services.py`, temperature 0 |
| Vector DB | Qdrant | Local Docker or Qdrant Cloud |
| Reranking | Cohere `rerank-english-v3.0` | Re-scores top-20 candidates down to top 5 |
| Observability | LangSmith | Tracing + presigned thumbs up/down feedback |
| PDF parsing | `pypdf` via LangChain `PyPDFLoader` | Page-level text extraction |
| DOCX parsing | `docx2txt` via LangChain `Docx2txtLoader` | Plain-text extraction |
| YouTube | LangChain `YoutubeLoader` | Transcript extraction |
| Web scraping | BeautifulSoup + httpx | HTML → text for URL ingest |

---

## Getting started

```bash
# clone
git clone https://github.com/yourname/rag-knowledge-base
cd rag-knowledge-base

# start Qdrant locally (runs at http://localhost:6333)
docker compose up qdrant -d

# backend — uv manages the virtualenv and Python version automatically
cp .env.example backend/.env   # fill in your API keys
cd backend
uv sync
uv run uvicorn api.main:app --reload

# frontend (separate terminal)
cd ../frontend
npm install
npm run dev
```

Required API keys (add to `backend/.env`):
- `OPENAI_API_KEY` — [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- `QDRANT_URL` — `http://localhost:6333` for local Docker, or your [Qdrant Cloud](https://cloud.qdrant.io) URL
- `QDRANT_API_KEY` — leave empty for local; fill in for Qdrant Cloud
- `QDRANT_COLLECTION_NAME` — any name you choose, e.g. `rag-knowledge-base`
- `COHERE_API_KEY` — [dashboard.cohere.com/api-keys](https://dashboard.cohere.com/api-keys)
- `LANGSMITH_API_KEY` — [smith.langchain.com](https://smith.langchain.com)
- `ANTHROPIC_API_KEY` — optional, only needed if swapping to Claude

---

## Deployment notes

Backend runs on **Google Cloud Run**, outbound HTTP requests to external sites (Medium, YouTube, etc.) are blocked or unreliable. URL and YouTube ingestion depends on those fetches, so it must be turned off in that environment.

Set this on your deployed backend service:

```
ENABLE_URL_INGEST=false
```

With that flag disabled:

- `POST /ingest/url` returns **503** with a clear error message instead of an unhandled 500.
- The frontend reads `url_ingest_enabled` from `GET /health` and **disables the URL input**, showing an explanatory message under the field.
- **PDF/DOCX upload and chat continue to work** on hosted — only URL/YouTube ingest is affected.

Locally, `ENABLE_URL_INGEST` defaults to `true` (or omit it entirely). The URL input stays enabled.