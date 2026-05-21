"use client";

import { useRef, useState } from "react";
import { ingestFile } from "@/lib/api";
import type { AsyncStatus } from "@/hooks/types";

export function useFileIngest(onIngested: (label: string) => void) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [status, setStatus] = useState<AsyncStatus>("idle");
  const [errorMsg, setErrorMsg] = useState("");

  const handleChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setStatus("loading");
    setErrorMsg("");
    try {
      await ingestFile(file);
      onIngested(file.name);
      setStatus("success");
    } catch (err) {
      setErrorMsg(err instanceof Error ? err.message : "Upload failed");
      setStatus("error");
    } finally {
      if (inputRef.current) inputRef.current.value = "";
    }
  };

  const openFilePicker = () => inputRef.current?.click();

  return { inputRef, status, errorMsg, handleChange, openFilePicker };
}
