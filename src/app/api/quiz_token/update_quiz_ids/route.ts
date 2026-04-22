import { z } from "zod";

import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { updateTokenQuizIds } from "@/server/services/quiz-service";

const schema = z.object({
  tokenId: z.string().min(1),
  quizIds: z.array(z.string()).default([]),
});

export async function POST(request: Request) {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    const body = await parseJsonBody(request, schema);
    await updateTokenQuizIds(body.tokenId, body.quizIds);
    return { success: true };
  });
}
