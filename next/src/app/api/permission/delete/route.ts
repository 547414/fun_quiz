import { eq } from "drizzle-orm";
import { z } from "zod";

import { db } from "@/db";
import { permissionAssigns, permissions } from "@/db/schema/core";
import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";

const schema = z.object({
  permissionId: z.string().min(1),
});

export async function POST(request: Request) {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN"]);
    const { permissionId } = await parseJsonBody(request, schema);
    await db.delete(permissionAssigns).where(eq(permissionAssigns.permissionId, permissionId));
    await db.delete(permissions).where(eq(permissions.id, permissionId));
    return { success: true };
  });
}
