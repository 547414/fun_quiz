import { z } from "zod";

import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { getQuizResult } from "@/server/services/quiz-service";

const schema = z.object({
  token: z.string().min(1),
  resultId: z.string().min(1),
});

export async function POST(request: Request) {
  return withApi(async () => {
    const { token, resultId } = await parseJsonBody(request, schema);
    return getQuizResult(token, resultId);
  });
}
