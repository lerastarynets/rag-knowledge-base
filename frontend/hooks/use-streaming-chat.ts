"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { parseFeedbackHeaders, streamChat } from "@/lib/api";
import type { ChatMessage } from "@/lib/api";

export function useStreamingChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const sessionId = useRef<string>(crypto.randomUUID());
  const isStreamingRef = useRef(false);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    return () => {
      abortRef.current?.abort();
    };
  }, []);

  const sendMessage = useCallback(async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed || isStreamingRef.current) return;

    const userMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: trimmed,
    };

    const assistantId = crypto.randomUUID();
    const assistantMsg: ChatMessage = {
      id: assistantId,
      role: "assistant",
      content: "",
      isStreaming: true,
    };

    setMessages((prev) => [...prev, userMsg, assistantMsg]);
    isStreamingRef.current = true;
    setIsStreaming(true);

    const controller = new AbortController();
    abortRef.current = controller;

    let reader: ReadableStreamDefaultReader<Uint8Array> | undefined;

    try {
      const response = await streamChat(
        trimmed,
        sessionId.current,
        controller.signal
      );
      const feedbackUrls = parseFeedbackHeaders(response);
      if (feedbackUrls) {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId ? { ...m, feedbackUrls } : m
          )
        );
      }

      reader = response.body?.getReader();
      if (!reader) throw new Error("No response body");
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId ? { ...m, content: m.content + chunk } : m
          )
        );
      }

      const tail = decoder.decode();
      if (tail) {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId ? { ...m, content: m.content + tail } : m
          )
        );
      }
    } catch (err) {
      if (controller.signal.aborted) return;
      const msg =
        err instanceof Error ? err.message : "Could not reach backend.";
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantId
            ? { ...m, content: `Error: ${msg}`, isStreaming: false }
            : m
        )
      );
    } finally {
      await reader?.cancel().catch(() => {});
      isStreamingRef.current = false;
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantId ? { ...m, isStreaming: false } : m
        )
      );
      setIsStreaming(false);
    }
  }, []);

  return { messages, isStreaming, sendMessage };
}
