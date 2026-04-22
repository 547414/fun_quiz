import { beforeEach, describe, expect, it, vi } from "vitest";

const repo = vi.hoisted(() => ({
  findQuizTokenByValue: vi.fn(),
  listAllowedQuizIdsByTokenId: vi.fn(),
  findQuizById: vi.fn(),
  listQuizQuestions: vi.fn(),
  listQuizOutcomes: vi.fn(),
  findOutcomeByCode: vi.fn(),
  createQuizResultWithTokenUsage: vi.fn(),
  updateQuizTokenUsage: vi.fn(),
  findQuizResultById: vi.fn(),
  updateQuizTokenStatus: vi.fn(),
  listQuizzesByTokenId: vi.fn(),
  listQuizResultsByTokenId: vi.fn(),
  listPublishedQuizzes: vi.fn(),
  listQuizHistoryByTokenId: vi.fn(),
  attachQuizIdsToToken: vi.fn(),
  createQuizToken: vi.fn(),
  deleteQuiz: vi.fn(),
  listQuizzes: vi.fn(),
  listQuizTokens: vi.fn(),
  replaceQuizOutcomes: vi.fn(),
  replaceQuizQuestions: vi.fn(),
  saveQuiz: vi.fn(),
}));

vi.mock("@/server/repositories/quiz-repository", () => repo);

describe("quiz-service integration-like behavior", async () => {
  const service = await import("@/server/services/quiz-service");

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("submitQuiz 会校验token授权并扣减次数", async () => {
    repo.findQuizTokenByValue.mockResolvedValue({
      id: "token1",
      status: "active",
      usedCount: 0,
      expiresAt: null,
    });
    repo.listQuizzesByTokenId.mockResolvedValue([{ id: "quiz1", status: "published" }]);
    repo.listAllowedQuizIdsByTokenId.mockResolvedValue(["quiz1"]);
    repo.findQuizById.mockResolvedValue({
      id: "quiz1",
      quizType: "score",
      status: "published",
      algoConfig: { total_max: 10 },
      specialRules: [],
    });
    repo.listQuizQuestions.mockResolvedValue([
      {
        seq: 1,
        isHidden: false,
        options: [{ key: "A", score: 10 }],
      },
    ]);
    repo.listQuizOutcomes.mockResolvedValue([
      { code: "OUTCOME_A", isFallback: false, isSpecial: false, matchConfig: { score_min: 5, score_max: 20 } },
    ]);
    repo.findOutcomeByCode.mockResolvedValue({ id: "outcome_id", code: "OUTCOME_A" });
    repo.createQuizResultWithTokenUsage.mockResolvedValue({ id: "token1", status: "active" });

    const result = await service.submitQuiz({
      token: "abc",
      quizId: "quiz1",
      answers: [{ questionSeq: 1, optionCode: "A" }],
    });

    expect(result.resultId).toBeTruthy();
    expect(repo.createQuizResultWithTokenUsage).toHaveBeenCalledTimes(1);
  });

  it("submitQuiz 在并发耗尽时返回 token exhausted", async () => {
    repo.findQuizTokenByValue.mockResolvedValue({
      id: "token1",
      status: "active",
      usedCount: 0,
      expiresAt: null,
    });
    repo.listQuizzesByTokenId.mockResolvedValue([{ id: "quiz1", status: "published" }]);
    repo.listAllowedQuizIdsByTokenId.mockResolvedValue(["quiz1"]);
    repo.findQuizById.mockResolvedValue({
      id: "quiz1",
      quizType: "score",
      status: "published",
      algoConfig: { total_max: 10 },
      specialRules: [],
    });
    repo.listQuizQuestions.mockResolvedValue([{ seq: 1, isHidden: false, options: [{ key: "A", score: 10 }] }]);
    repo.listQuizOutcomes.mockResolvedValue([{ code: "OUTCOME_A", isFallback: false, isSpecial: false, matchConfig: { score_min: 5, score_max: 20 } }]);
    repo.findOutcomeByCode.mockResolvedValue({ id: "outcome_id", code: "OUTCOME_A" });
    repo.createQuizResultWithTokenUsage.mockResolvedValue(null);

    await expect(
      service.submitQuiz({
        token: "abc",
        quizId: "quiz1",
        answers: [{ questionSeq: 1, optionCode: "A" }],
      }),
    ).rejects.toThrow();
  });

  it("getQuizResult 必须校验结果归属token", async () => {
    repo.findQuizTokenByValue.mockResolvedValue({
      id: "token1",
      status: "active",
      usedCount: 1,
      expiresAt: null,
    });
    repo.listQuizzesByTokenId.mockResolvedValue([{ id: "quiz1", status: "published" }]);
    repo.findQuizResultById.mockResolvedValue({
      id: "result1",
      tokenId: "token2",
      quizId: "quiz1",
      outcomeCode: "OUT_A",
      score: 88,
    });

    await expect(service.getQuizResult("token_value", "result1")).rejects.toThrow();
  });
});
