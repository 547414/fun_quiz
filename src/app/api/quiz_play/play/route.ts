import { z } from "zod";

import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { quizPlay } from "@/server/services/quiz-service";

const schema = z.object({
  token: z.string().min(1),
  quizId: z.string().min(1),
});

export async function POST(request: Request) {
  return withApi(async () => {
    const body = await parseJsonBody(request, schema);
    return quizPlay(body.token, body.quizId);
  });
}
