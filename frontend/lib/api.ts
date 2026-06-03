const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

// ---------------------------------------------------------------------------
// Shared types
// ---------------------------------------------------------------------------

export interface IngestJobResponse {
  job_id: string;
  status: "queued";
}

export interface FeedbackUrls {
  up: string;
  down: string;
}

export interface Citation {
  filename: string;
  page: number | null;
  url: string | null;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  isStreaming?: boolean;
  citations: Citation[];
  feedbackUrls?: FeedbackUrls;
}

// ---------------------------------------------------------------------------
// Ingest
// ---------------------------------------------------------------------------

export async function ingestFile(file: File): Promise<IngestJobResponse> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${BASE_URL}/ingest/file`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) throw new Error(`Ingest file failed: ${res.status}`);
  return res.json() as Promise<IngestJobResponse>;
}

export async function ingestUrl(url: string): Promise<IngestJobResponse> {
  const res = await fetch(`${BASE_URL}/ingest/url`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  if (!res.ok) throw new Error(`Ingest URL failed: ${res.status}`);
  return res.json() as Promise<IngestJobResponse>;
}

// ---------------------------------------------------------------------------
// Chat
// ---------------------------------------------------------------------------

/**
 * Opens a streaming fetch to POST /chat/.
 * The caller is responsible for reading `response.body`.
 */
export async function streamChat(
  message: string,
  sessionId: string
): Promise<Response> {
  const res = await fetch(`${BASE_URL}/chat/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId }),
  });
  if (!res.ok) throw new Error(`Chat failed: ${res.status}`);
  return res;
}

// ---------------------------------------------------------------------------
// Feedback (LangSmith presigned URLs — no API key required)
// ---------------------------------------------------------------------------

export function parseFeedbackHeaders(response: Response): FeedbackUrls | null {
  const up = response.headers.get("X-Feedback-Up");
  const down = response.headers.get("X-Feedback-Down");
  if (!up || !down) return null;
  return { up, down };
}

export async function submitLangSmithFeedback(
  presignedUrl: string,
  comment?: string
): Promise<void> {
  const res = await fetch(presignedUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      score: 1,
      ...(comment ? { comment } : {}),
    }),
  });
  if (!res.ok) throw new Error(`Feedback failed: ${res.status}`);
}
