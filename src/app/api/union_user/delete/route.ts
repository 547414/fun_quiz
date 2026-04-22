import { eq } from "drizzle-orm";
import { z } from "zod";

import { db } from "@/db";
import { userRoles, webUsers } from "@/db/schema/core";
import { AppError } from "@/lib/errors";
import { requireAuth } from "@/lib/auth/guard";
import { clearAuthCookies } from "@/lib/auth/session";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { queryRoleCodesByUserId } from "@/server/repositories/user-repository";
import { revokeUserSessions } from "@/server/services/auth-service";

const schema = z.object({
  unionUserId: z.string().optional(),
});

export async function POST(request: Request) {
  return withApi(async () => {
    const current = await requireAuth();
    const body = await parseJsonBody(request, schema);
    const targetUnionUserId = body.unionUserId ?? current.unionUserId;
    const isDeletingSelf = targetUnionUserId === current.unionUserId;
    const isSuperAdmin = current.roleCodes.includes("SUPER_ADMIN");
    if (!isDeletingSelf && !isSuperAdmin) {
      throw new AppError("Forbidden", 403);
    }

    const targetRoles = await queryRoleCodesByUserId(targetUnionUserId);
    if (targetRoles.includes("SUPER_ADMIN")) {
      throw new AppError("SUPER_ADMIN account cannot be deleted", 403);
    }

    await revokeUserSessions(targetUnionUserId);
    await db.delete(userRoles).where(eq(userRoles.userId, targetUnionUserId));
    await db.delete(webUsers).where(eq(webUsers.id, targetUnionUserId));
    if (isDeletingSelf) {
      await clearAuthCookies(current.space);
    }
    return { success: true };
  });
}
