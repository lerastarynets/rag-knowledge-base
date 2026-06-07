"use client";

import { useEffect, useState } from "react";
import { fetchHealth } from "@/lib/api";

export function useUrlIngestCapability() {
  const [urlIngestEnabled, setUrlIngestEnabled] = useState<boolean | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    fetchHealth()
      .then((health) => {
        if (!cancelled) {
          setUrlIngestEnabled(health.url_ingest_enabled);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setUrlIngestEnabled(true);
        }
      })
      .finally(() => {
        if (!cancelled) {
          setIsLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return { urlIngestEnabled, isLoading };
}
