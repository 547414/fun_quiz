export class AppError extends Error {
  readonly code: number;
  readonly detail?: unknown;

  constructor(message: string, code = 500, detail?: unknown) {
    super(message);
    this.name = "AppError";
    this.code = code;
    this.detail = detail;
  }
}

export function toErrorMessage(error: unknown): string {
  if (error instanceof Error) return error.message;
  if (typeof error === "string") return error;
  return "Unknown error";
}
