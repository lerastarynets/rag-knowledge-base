"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Send } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Message } from "@/components/Message";
import { useStreamingChat } from "@/hooks/use-streaming-chat";

export function Chat() {
  const { messages, isStreaming, sendMessage } = useStreamingChat();
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = useCallback(() => {
    if (!input.trim() || isStreaming) return;
    sendMessage(input);
    setInput("");
  }, [input, isStreaming, sendMessage]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-1 flex-col overflow-hidden bg-background">
      <div className="flex-1 overflow-y-auto py-6">
        {messages.length === 0 ? (
          <EmptyState />
        ) : (
          <div className="flex flex-col gap-6">
            {messages.map((msg) => (
              <Message key={msg.id} message={msg} />
            ))}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="border-t border-border bg-background px-4 py-3">
        <div className="flex items-end gap-2">
          <Textarea
            rows={1}
            placeholder="Ask anything… (Enter to send, Shift+Enter for newline)"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isStreaming}
            className={cn(
              "max-h-40 min-h-[40px] flex-1 py-2.5 text-sm leading-relaxed",
              "bg-card text-foreground caret-foreground focus-visible:ring-ring/60"
            )}
          />
          <Button
            size="icon"
            onClick={handleSend}
            disabled={!input.trim() || isStreaming}
            aria-label="Send"
            className="mb-0.5 size-9 shrink-0"
          >
            <Send className="size-4" />
          </Button>
        </div>
        <p className="mt-1.5 text-center text-[10px] text-muted-foreground">
          Answers are grounded in your uploaded sources.
        </p>
      </div>
    </div>
  );
}

function EmptyState() {
  return (
    <div className="flex h-full flex-col items-center justify-center gap-3 px-6 text-center">
      <div className="rounded-full border border-border bg-muted p-3">
        <Send className="size-5 text-muted-foreground" />
      </div>
      <p className="text-sm font-medium text-foreground">Start a conversation</p>
      <p className="max-w-xs text-xs text-muted-foreground">
        Upload documents or URLs in the sidebar, then ask questions about them.
      </p>
    </div>
  );
}
