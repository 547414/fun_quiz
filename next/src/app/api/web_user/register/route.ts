import { z } from "zod";
import { and, eq } from "drizzle-orm";

import { db } from "@/db";
import { inviteCodes } from "@/db/schema/core";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { registerWebUser } from "@/server/services/auth-service";

const schema = z.object({
  account: z.string().min(3),
  name: z.string().min(1),
  password: z.string().min(6),
  inviteCode: z.string().min(1),
});

export async function POST(request: Request) {
  return withApi(async () => {
    const body = await parseJsonBody(request, schema);
    const [invite] = await db
      .select()
      .from(inviteCodes)
      .where(and(eq(inviteCodes.code, body.inviteCode), eq(inviteCodes.enabled, true)))
      .limit(1);
    if (!invite) {
      throw new Error("invite code invalid");
    }
    if (invite.expiresAt && invite.expiresAt.getTime() < Date.now()) {
      throw new Error("invite code expired");
    }
    if (invite.usedTimes >= invite.maxUseTimes) {
      throw new Error("invite code exhausted");
    }
    await db
      .update(inviteCodes)
      .set({
        usedTimes: invite.usedTimes + 1,
        updatedAt: new Date(),
      })
      .where(eq(inviteCodes.id, invite.id));
    return registerWebUser(body);
  });
}
