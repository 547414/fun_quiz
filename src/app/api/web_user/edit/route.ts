import { z } from "zod";

import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { updateWebUser } from "@/server/repositories/user-repository";

const schema = z.object({
  userId: z.string().min(1),
  name: z.string().optional(),
  enabled: z.boolean().optional(),
  avatarFileInfo: z.string().nullable().optional(),
});

export async function POST(request: Request) {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    const body = await parseJsonBody(request, schema);
    await updateWebUser(body.userId, {
      name: body.name,
      enabled: body.enabled,
      avatarFileInfo: body.avatarFileInfo ?? null,
    });
    return { success: true };
  });
}
