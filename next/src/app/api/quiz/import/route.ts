import { z } from "zod";

import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { editQuiz, saveOutcomes, saveQuestions } from "@/server/services/quiz-service";

const schema = z.object({
  definition: z.object({
    quiz: z.record(z.string(), z.unknown()),
    questions: z.array(z.record(z.string(), z.unknown())).default([]),
    outcomes: z.array(z.record(z.string(), z.unknown())).default([]),
  }),
});

export async function POST(request: Request) {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    const body = await parseJsonBody(request, schema);
    const saved = await editQuiz(body.definition.quiz);
    await saveQuestions(saved.id, body.definition.questions);
    await saveOutcomes(saved.id, body.definition.outcomes);
    return {
      quiz_id: saved.id,
    };
  });
}
