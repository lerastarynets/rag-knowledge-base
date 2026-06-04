"use client";

import { FileText, Link } from "lucide-react";
import type { Citation } from "@/lib/api";
import { cn, extractDomain } from "@/lib/utils";

export function CitationChip({ filename, page, url }: Citation) {
  const label = url ? extractDomain(url) : filename;
  const tooltip = [filename, page != null ? `p. ${page}` : null]
    .filter(Boolean)
    .join(" · ");

  const handleClick = () => {
    if (url) {
      window.open(url, "_blank", "noopener,noreferrer");
    }
  };

  return (
    <div className="group relative inline-flex">
      <button
        onClick={handleClick}
        title={tooltip}
        className={cn(
          "inline-flex items-center gap-1 rounded-full border border-border",
          "bg-muted/50 px-2 py-0.5 text-xs text-muted-foreground",
          "transition-colors hover:bg-muted hover:text-foreground",
          url ? "cursor-pointer" : "cursor-default"
        )}
      >
        {url ? (
          <Link className="size-3 shrink-0" />
        ) : (
          <FileText className="size-3 shrink-0" />
        )}
        <span className="max-w-[120px] truncate">{label}</span>
      </button>

      {!url && (
        <div
          className={cn(
            "pointer-events-none absolute bottom-full left-0 z-10 mb-1.5",
            "hidden group-hover:block",
            "rounded-md border border-border bg-popover px-2.5 py-1.5",
            "text-xs text-popover-foreground shadow-md whitespace-nowrap"
          )}
        >
          {tooltip}
        </div>
      )}
    </div>
  );
}
