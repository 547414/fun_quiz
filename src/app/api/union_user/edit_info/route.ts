import { z } from "zod";

import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { updateWebUser } from "@/server/repositories/user-repository";

const schema = z.object({
  name: z.string().optional(),
  avatarFileInfo: z.string().nullable().optional(),
});

export async function POST(request: Request) {
  return withApi(async () => {
    const current = await requireAuth();
    const body = await parseJsonBody(request, schema);
    await updateWebUser(current.webUserId, {
      name: body.name,
      avatarFileInfo: body.avatarFileInfo ?? null,
    });
    return { success: true };
  });
}
