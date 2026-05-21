"use client";

import { useState } from "react";
import { submitFeedback } from "@/lib/api";

export function useMessageFeedback(messageId: string) {
  const [feedback, setFeedback] = useState<"up" | "down" | null>(null);

  const submit = async (rating: "up" | "down") => {
    if (feedback !== null) return;
    setFeedback(rating);
    try {
      // TODO: replace messageId with the real message_id returned by the backend
      await submitFeedback({ message_id: messageId, rating });
    } catch {
      // silently fail; feedback is best-effort
    }
  };

  return { feedback, submit };
}
