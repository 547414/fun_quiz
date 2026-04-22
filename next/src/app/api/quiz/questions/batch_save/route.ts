import { z } from "zod";

import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { saveQuestions } from "@/server/services/quiz-service";

const schema = z.object({
  quizId: z.string().min(1),
  questionList: z.array(z.record(z.string(), z.unknown())).default([]),
});

export async function POST(request: Request) {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    const body = await parseJsonBody(request, schema);
    await saveQuestions(body.quizId, body.questionList);
    return { success: true };
  });
}
