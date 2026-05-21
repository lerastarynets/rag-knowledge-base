"use client";

import {
  Upload,
  Link,
  CheckCircle2,
  AlertCircle,
  Loader2,
  FileText,
  Globe,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useFileIngest } from "@/hooks/use-file-ingest";
import { useUrlIngest } from "@/hooks/use-url-ingest";
import { useIngestedSources } from "@/hooks/use-ingested-sources";
import type { AsyncStatus } from "@/hooks/types";

export function Sidebar() {
  const { sources, addSource } = useIngestedSources();

  return (
    <aside className="flex h-screen w-[280px] shrink-0 flex-col border-r border-border bg-sidebar">
      <div className="border-b border-border px-4 py-3">
        <h1 className="text-sm font-semibold tracking-tight text-sidebar-foreground">
          RAG Knowledge Base
        </h1>
      </div>

      <div className="flex flex-col gap-4 p-4">
        <p className="text-xs font-medium uppercase tracking-widest text-muted-foreground">
          Add Sources
        </p>

        <FileUpload onIngested={(label) => addSource(label, "file")} />
        <UrlIngest onIngested={(label) => addSource(label, "url")} />
      </div>

      <div className="mx-4 border-t border-border" />

      <div className="flex flex-1 flex-col gap-2 overflow-y-auto p-4">
        <p className="text-xs font-medium uppercase tracking-widest text-muted-foreground">
          Ingested Sources
        </p>

        {sources.length === 0 ? (
          <p className="mt-2 text-xs text-muted-foreground">
            No sources yet. Upload a file or paste a URL above.
          </p>
        ) : (
          <ul className="flex flex-col gap-1">
            {sources.map((src) => (
              <li
                key={src.id}
                className="flex items-center gap-2 rounded-md px-2 py-1.5 text-xs text-sidebar-foreground hover:bg-sidebar-accent"
              >
                {src.type === "file" ? (
                  <FileText className="size-3.5 shrink-0 text-muted-foreground" />
                ) : (
                  <Globe className="size-3.5 shrink-0 text-muted-foreground" />
                )}
                <span className="truncate">{src.label}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </aside>
  );
}

function FileUpload({ onIngested }: { onIngested: (label: string) => void }) {
  const { inputRef, status, errorMsg, handleChange, openFilePicker } =
    useFileIngest(onIngested);

  return (
    <div className="flex flex-col gap-1.5">
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.docx"
        className="hidden"
        onChange={handleChange}
      />
      <Button
        variant="outline"
        size="sm"
        className="w-full justify-start gap-2"
        onClick={openFilePicker}
        disabled={status === "loading"}
      >
        {status === "loading" ? (
          <Loader2 className="size-3.5 animate-spin" />
        ) : (
          <Upload className="size-3.5" />
        )}
        Upload PDF / DOCX
      </Button>

      <IngestStatusLine
        status={status}
        successText="✓ Ingested"
        errorText={errorMsg}
      />
    </div>
  );
}

function UrlIngest({ onIngested }: { onIngested: (label: string) => void }) {
  const { url, setUrl, status, errorMsg, handleSubmit } = useUrlIngest(onIngested);

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-1.5">
      <div className="flex gap-1.5">
        <Input
          type="url"
          placeholder="https://example.com"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="h-8 text-xs"
          disabled={status === "loading"}
        />
        <Button
          type="submit"
          size="icon"
          variant="outline"
          className="size-8 shrink-0"
          disabled={status === "loading" || !url.trim()}
          aria-label="Add URL"
        >
          {status === "loading" ? (
            <Loader2 className="size-3.5 animate-spin" />
          ) : (
            <Link className="size-3.5" />
          )}
        </Button>
      </div>

      <IngestStatusLine
        status={status}
        successText="✓ Ingested"
        errorText={errorMsg}
      />
    </form>
  );
}

function IngestStatusLine({
  status,
  successText,
  errorText,
}: {
  status: AsyncStatus;
  successText: string;
  errorText: string;
}) {
  if (status === "success") {
    return (
      <p className={cn("flex items-center gap-1 text-xs text-green-400")}>
        <CheckCircle2 className="size-3" />
        {successText}
      </p>
    );
  }
  if (status === "error") {
    return (
      <p className={cn("flex items-center gap-1 text-xs text-destructive")}>
        <AlertCircle className="size-3" />
        {errorText}
      </p>
    );
  }
  return null;
}
