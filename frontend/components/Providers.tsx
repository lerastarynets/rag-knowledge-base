"use client";

import { CopilotKit } from "@copilotkit/react-core";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <CopilotKit enableInspector={false} runtimeUrl={process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}>
      {children}
    </CopilotKit>
  );
}
