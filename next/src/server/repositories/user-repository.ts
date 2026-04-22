import { and, eq, inArray } from "drizzle-orm";

import { db } from "@/db";
import { roles, userRoles, webUsers } from "@/db/schema/core";

export async function findWebUserByAccount(account: string) {
  const [user] = await db.select().from(webUsers).where(eq(webUsers.account, account)).limit(1);
  return user ?? null;
}

export async function findWebUserById(userId: string) {
  const [user] = await db.select().from(webUsers).where(eq(webUsers.id, userId)).limit(1);
  return user ?? null;
}

export async function createWebUser(input: {
  id: string;
  account: string;
  name: string;
  passwordSalt: string;
  passwordHash: string;
}) {
  await db.insert(webUsers).values(input);
}

export async function updateWebUser(userId: string, input: Partial<typeof webUsers.$inferInsert>) {
  await db
    .update(webUsers)
    .set({
      ...input,
      updatedAt: new Date(),
    })
    .where(eq(webUsers.id, userId));
}

export async function queryRoleCodesByUserId(userId: string): Promise<string[]> {
  const roleMappings = await db.select().from(userRoles).where(eq(userRoles.userId, userId));
  if (!roleMappings.length) return [];
  const roleIds = roleMappings.map((item) => item.roleId);
  const roleRows = await db.select().from(roles).where(inArray(roles.id, roleIds));
  return roleRows.filter((row) => row.enabled).map((row) => row.code);
}

export async function bindRoleToUser(input: { id: string; userId: string; roleId: string }) {
  const [exists] = await db
    .select()
    .from(userRoles)
    .where(and(eq(userRoles.userId, input.userId), eq(userRoles.roleId, input.roleId)))
    .limit(1);
  if (exists) return;
  await db.insert(userRoles).values(input);
}

export async function replaceUserRoles(userId: string, roleIds: string[]) {
  await db.delete(userRoles).where(eq(userRoles.userId, userId));
  if (!roleIds.length) return;
  await db.insert(userRoles).values(
    roleIds.map((roleId) => ({
      id: `${userId}_${roleId}`,
      userId,
      roleId,
    })),
  );
}
