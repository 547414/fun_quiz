import { z } from "zod";

import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { removeQuiz } from "@/server/services/quiz-service";

const schema = z.object({
  quizId: z.string().min(1),
});

export async function POST(request: Request) {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    const { quizId } = await parseJsonBody(request, schema);
    await removeQuiz(quizId);
    return { success: true };
  });
}
