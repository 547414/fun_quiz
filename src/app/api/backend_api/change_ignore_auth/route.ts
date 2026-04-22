import { eq } from "drizzle-orm";
import { z } from "zod";

import { db } from "@/db";
import { backendApis } from "@/db/schema/core";
import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";

const schema = z.object({
  backendApiId: z.string().min(1),
  ignoreAuth: z.boolean(),
});

export async function POST(request: Request) {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN"]);
    const body = await parseJsonBody(request, schema);
    await db
      .update(backendApis)
      .set({
        ignoreAuth: body.ignoreAuth,
        updatedAt: new Date(),
      })
      .where(eq(backendApis.id, body.backendApiId));
    return { success: true };
  });
}
