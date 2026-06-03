"use client";

import { ThumbsUp, ThumbsDown } from "lucide-react";
import { cn } from "@/lib/utils";
import { CitationChip } from "@/components/CitationChip";
import { useMessageFeedback } from "@/hooks/use-message-feedback";
import type { ChatMessage } from "@/lib/api";

interface MessageProps {
  message: ChatMessage;
}

export function Message({ message }: MessageProps) {
  const isUser = message.role === "user";

  return isUser ? (
    <UserBubble content={message.content} />
  ) : (
    <AssistantBubble message={message} />
  );
}

function UserBubble({ content }: { content: string }) {
  return (
    <div className="flex justify-end px-4">
      <div
        className={cn(
          "max-w-[75%] rounded-2xl rounded-tr-sm px-4 py-2.5",
          "bg-primary text-primary-foreground text-sm leading-relaxed",
          "whitespace-pre-wrap break-words"
        )}
      >
        {content}
      </div>
    </div>
  );
}

function AssistantBubble({ message }: { message: ChatMessage }) {
  const { feedback, submit, canSubmit } = useMessageFeedback(
    message.feedbackUrls
  );

  return (
    <div className="flex flex-col gap-2 px-4">
      <div
        className={cn(
          "max-w-[85%] rounded-2xl rounded-tl-sm px-4 py-2.5",
          "bg-card border border-border text-sm leading-relaxed",
          "text-card-foreground whitespace-pre-wrap break-words"
        )}
      >
        {message.content}
        {message.isStreaming && (
          <span className="ml-0.5 inline-block h-[1em] w-0.5 translate-y-[2px] animate-pulse bg-foreground/70" />
        )}
      </div>

      {message.citations.length > 0 && (
        <div className="flex max-w-[85%] flex-wrap gap-1.5 pl-1">
          {message.citations.map((c, i) => (
            <CitationChip
              key={i}
              filename={c.filename}
              page={c.page}
              url={c.url}
            />
          ))}
        </div>
      )}

      {!message.isStreaming && canSubmit && (
        <div className="flex items-center gap-1 pl-1">
          <button
            onClick={() => submit("up")}
            disabled={feedback !== null}
            aria-label="Thumbs up"
            className={cn(
              "rounded-md p-1 transition-colors",
              feedback === "up"
                ? "text-green-400"
                : "text-muted-foreground hover:text-foreground",
              feedback === "down" && "opacity-30"
            )}
          >
            <ThumbsUp className="size-3.5" />
          </button>
          <button
            onClick={() => submit("down")}
            disabled={feedback !== null}
            aria-label="Thumbs down"
            className={cn(
              "rounded-md p-1 transition-colors",
              feedback === "down"
                ? "text-red-400"
                : "text-muted-foreground hover:text-foreground",
              feedback === "up" && "opacity-30"
            )}
          >
            <ThumbsDown className="size-3.5" />
          </button>
        </div>
      )}
    </div>
  );
}
