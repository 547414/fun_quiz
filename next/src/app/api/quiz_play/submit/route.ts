import { z } from "zod";

import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { submitQuiz } from "@/server/services/quiz-service";

const answerSchema = z.object({
  questionId: z.string().optional(),
  questionSeq: z.number().optional(),
  optionCode: z.string().optional(),
  score: z.number().optional(),
});

const schema = z.object({
  token: z.string().min(1),
  quizId: z.string().min(1),
  answers: z.array(answerSchema).default([]),
});

export async function POST(request: Request) {
  return withApi(async () => {
    const body = await parseJsonBody(request, schema);
    return submitQuiz(body);
  });
}
