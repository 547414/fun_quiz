import { z } from "zod";

import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { quizEntry } from "@/server/services/quiz-service";

const schema = z.object({
  token: z.string().min(1),
});

export async function POST(request: Request) {
  return withApi(async () => {
    const { token } = await parseJsonBody(request, schema);
    const entry = await quizEntry(token);
    const isDemoToken = entry.token.token === "demo";
    return {
      status: entry.token.status,
      maxUses: isDemoToken ? null : entry.token.maxUses,
      usedCount: entry.token.usedCount,
      hasHistory: entry.token.usedCount > 0,
      max_uses: isDemoToken ? null : entry.token.maxUses,
      used_count: entry.token.usedCount,
      has_history: entry.token.usedCount > 0,
    };
  });
}
