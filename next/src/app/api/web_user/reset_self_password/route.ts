import { z } from "zod";

import { requireAuth } from "@/lib/auth/guard";
import { hashPassword, verifyPassword } from "@/lib/auth/password";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { findWebUserById, updateWebUser } from "@/server/repositories/user-repository";

const schema = z.object({
  oldPassword: z.string().min(6),
  newPassword: z.string().min(6),
  newPasswordRepeat: z.string().min(6),
});

export async function POST(request: Request) {
  return withApi(async () => {
    const current = await requireAuth();
    const body = await parseJsonBody(request, schema);
    const user = await findWebUserById(current.webUserId);
    if (!user) throw new Error("user not found");
    if (body.newPassword !== body.newPasswordRepeat) {
      throw new Error("new password repeat does not match");
    }
    if (body.oldPassword === body.newPassword) {
      throw new Error("new password cannot be old password");
    }
    const matchedOld = await verifyPassword(`${body.oldPassword}:${user.passwordSalt}`, user.passwordHash);
    if (!matchedOld) {
      throw new Error("old password invalid");
    }
    const passwordHash = await hashPassword(`${body.newPassword}:${user.passwordSalt}`);
    await updateWebUser(user.id, {
      passwordHash,
      resetPassword: false,
    });
    return { success: true };
  });
}
