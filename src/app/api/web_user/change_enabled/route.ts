import { z } from "zod";

import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { updateWebUser } from "@/server/repositories/user-repository";
import { revokeUserSessions } from "@/server/services/auth-service";

const schema = z.object({
  userId: z.string().min(1),
  enabled: z.boolean(),
});

export async function POST(request: Request) {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    const body = await parseJsonBody(request, schema);
    await updateWebUser(body.userId, { enabled: body.enabled });
    if (!body.enabled) {
      await revokeUserSessions(body.userId);
    }
    return { success: true };
  });
}
