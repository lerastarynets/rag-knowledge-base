"use client";

import { useState } from "react";
import type { IngestedSource } from "@/hooks/types";

export function useIngestedSources() {
  const [sources, setSources] = useState<IngestedSource[]>([]);

  const addSource = (label: string, type: IngestedSource["type"]) => {
    setSources((prev) => [
      ...prev,
      { id: crypto.randomUUID(), label, type },
    ]);
  };

  return { sources, addSource };
}
