"use client";

import { useState } from "react";
import { ingestUrl } from "@/lib/api";
import type { AsyncStatus } from "@/hooks/types";
import { extractDomain } from "@/lib/utils";

export function useUrlIngest(
  onIngested: (label: string) => void,
  urlIngestEnabled: boolean | null = true
) {
  const [url, setUrl] = useState("");
  const [status, setStatus] = useState<AsyncStatus>("idle");
  const [errorMsg, setErrorMsg] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim() || urlIngestEnabled === false) return;
    setStatus("loading");
    setErrorMsg("");
    try {
      await ingestUrl(url.trim());
      onIngested(extractDomain(url.trim()));
      setStatus("success");
      setUrl("");
    } catch (err) {
      setErrorMsg(err instanceof Error ? err.message : "Failed to ingest URL");
      setStatus("error");
    }
  };

  return { url, setUrl, status, errorMsg, handleSubmit };
}
