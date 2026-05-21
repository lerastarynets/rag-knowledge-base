export type AsyncStatus = "idle" | "loading" | "success" | "error";

export interface IngestedSource {
  id: string;
  label: string;
  type: "file" | "url";
}
