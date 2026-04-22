import { z } from "zod";

import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { registerWebUser } from "@/server/services/auth-service";

const schema = z.object({
  account: z.string().min(3),
  name: z.string().min(1),
  password: z.string().min(6).default("123456"),
});

export async function POST(request: Request) {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    const body = await parseJsonBody(request, schema);
    return registerWebUser(body);
  });
}
