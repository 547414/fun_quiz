import { eq } from "drizzle-orm";
import { z } from "zod";

import { db } from "@/db";
import { roles, userRoles } from "@/db/schema/core";
import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";

const schema = z.object({
  roleId: z.string().min(1),
});

export async function POST(request: Request) {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN"]);
    const body = await parseJsonBody(request, schema);
    await db.delete(userRoles).where(eq(userRoles.roleId, body.roleId));
    await db.delete(roles).where(eq(roles.id, body.roleId));
    return { success: true };
  });
}
