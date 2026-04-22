import { inArray } from "drizzle-orm";
import { z } from "zod";

import { db } from "@/db";
import { webUsers } from "@/db/schema/core";
import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { queryRoleCodesByUserId } from "@/server/repositories/user-repository";

const schema = z.object({
  userIdList: z.array(z.string()).default([]),
});

export async function POST(request: Request) {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    const { userIdList } = await parseJsonBody(request, schema);
    if (!userIdList.length) return [];
    const rows = await db
      .select({
        id: webUsers.id,
        account: webUsers.account,
        name: webUsers.name,
        enabled: webUsers.enabled,
        resetPassword: webUsers.resetPassword,
        tryCount: webUsers.tryCount,
        createdAt: webUsers.createdAt,
        updatedAt: webUsers.updatedAt,
      })
      .from(webUsers)
      .where(inArray(webUsers.id, userIdList));
    return Promise.all(
      rows.map(async (row) => ({
        ...row,
        roleCodes: await queryRoleCodesByUserId(row.id),
      })),
    );
  });
}
