"use client";

import { useState } from "react";
import { submitLangSmithFeedback } from "@/lib/api";
import type { FeedbackUrls } from "@/lib/api";

export function useMessageFeedback(feedbackUrls?: FeedbackUrls) {
  const [feedback, setFeedback] = useState<"up" | "down" | null>(null);

  const submit = async (rating: "up" | "down") => {
    if (feedback !== null || !feedbackUrls) return;
    setFeedback(rating);
    try {
      const url = rating === "up" ? feedbackUrls.up : feedbackUrls.down;
      await submitLangSmithFeedback(url);
    } catch {
      setFeedback(null);
    }
  };

  return { feedback, submit, canSubmit: Boolean(feedbackUrls) };
}
