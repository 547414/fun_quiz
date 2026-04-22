import { eq } from "drizzle-orm";
import { z } from "zod";

import { db } from "@/db";
import { organizations } from "@/db/schema/core";
import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";

const schema = z.object({ organizationId: z.string().min(1) });

export async function POST(request: Request) {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    const { organizationId } = await parseJsonBody(request, schema);
    await db.delete(organizations).where(eq(organizations.id, organizationId));
    return { success: true };
  });
}
