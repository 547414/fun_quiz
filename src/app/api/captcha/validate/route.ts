import { z } from "zod";

import { parseJsonBody } from "@/lib/request";
import { withApi } from "@/lib/http";

const schema = z.object({
  verifyId: z.string().min(1),
  clickData: z.array(z.object({ x: z.number(), y: z.number() })).optional(),
});

export async function POST(request: Request) {
  return withApi(async () => {
    await parseJsonBody(request, schema);
    return { passed: true };
  });
}
