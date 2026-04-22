import { z } from "zod";

import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { pageQuizTokens } from "@/server/services/quiz-service";

const schema = z.object({
  search: z.string().optional(),
  pageIndex: z.number().int().default(1),
  pageSize: z.number().int().default(20),
});

export async function POST(request: Request) {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    const contentLength = request.headers.get("content-length");
    const body = contentLength && Number(contentLength) > 0 ? await parseJsonBody(request, schema) : schema.parse({});
    return pageQuizTokens(body);
  });
}
