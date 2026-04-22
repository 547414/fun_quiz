import { z } from "zod";

import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { detailQuiz, editQuiz } from "@/server/services/quiz-service";

const schema = z.object({
  quizId: z.string().min(1),
  status: z.string().min(1),
});

export async function POST(request: Request) {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    const body = await parseJsonBody(request, schema);
    const current = await detailQuiz(body.quizId);
    await editQuiz({
      ...current,
      id: body.quizId,
      status: body.status,
    });
    return { success: true };
  });
}
