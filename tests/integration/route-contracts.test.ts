import { describe, expect, it, vi } from "vitest";

describe("route contracts", () => {
  it("quiz_play/entry/history returns page shape for invalid token", async () => {
    vi.resetModules();
    vi.doMock("@/server/services/quiz-service", () => ({
      getEntryHistoryPage: vi.fn().mockRejectedValue(new Error("Invalid token")),
    }));
    const { POST } = await import("@/app/api/quiz_play/entry/history/route");
    const response = await POST(
      new Request("http://localhost/api/quiz_play/entry/history", {
        method: "POST",
        body: JSON.stringify({ token: "invalid", pageIndex: 1, pageSize: 10 }),
        headers: { "content-type": "application/json" },
      }),
    );
    const json = (await response.json()) as { code: number; data: { total: number; list: unknown[] } };
    expect(json.code).toBe(200);
    expect(json.data.total).toBe(0);
    expect(Array.isArray(json.data.list)).toBe(true);
  });

  it("quiz_play/entry/quizzes returns page shape for invalid token", async () => {
    vi.resetModules();
    vi.doMock("@/server/services/quiz-service", () => ({
      getEntryQuizzes: vi.fn().mockRejectedValue(new Error("Invalid token")),
    }));
    const { POST } = await import("@/app/api/quiz_play/entry/quizzes/route");
    const response = await POST(
      new Request("http://localhost/api/quiz_play/entry/quizzes", {
        method: "POST",
        body: JSON.stringify({ token: "invalid", pageIndex: 1, pageSize: 10 }),
        headers: { "content-type": "application/json" },
      }),
    );
    const json = (await response.json()) as { code: number; data: { total: number; list: unknown[] } };
    expect(json.code).toBe(200);
    expect(json.data.total).toBe(0);
    expect(Array.isArray(json.data.list)).toBe(true);
  });
});
