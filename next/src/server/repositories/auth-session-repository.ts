import { and, eq, gt, isNull, or } from "drizzle-orm";

import { db } from "@/db";
import { authSessions, tokenBlacklists } from "@/db/schema/core";

type UpsertSessionInput = {
  id: string;
  unionUserId: string;
  scene: string;
  space: string;
  accessToken: string;
  refreshToken: string;
  currentRoleCode?: string | null;
  expiresAt?: Date | null;
  refreshExpiresAt?: Date | null;
};

export async function upsertAuthSession(input: UpsertSessionInput) {
  const [exists] = await db
    .select()
    .from(authSessions)
    .where(and(eq(authSessions.unionUserId, input.unionUserId), eq(authSessions.scene, input.scene), eq(authSessions.space, input.space)))
    .limit(1);

  if (exists) {
    await db
      .update(authSessions)
      .set({
        accessToken: input.accessToken,
        refreshToken: input.refreshToken,
        currentRoleCode: input.currentRoleCode ?? null,
        expiresAt: input.expiresAt ?? null,
        refreshExpiresAt: input.refreshExpiresAt ?? null,
        updatedAt: new Date(),
      })
      .where(eq(authSessions.id, exists.id));
    return;
  }

  await db.insert(authSessions).values({
    id: input.id,
    unionUserId: input.unionUserId,
    scene: input.scene,
    space: input.space,
    accessToken: input.accessToken,
    refreshToken: input.refreshToken,
    currentRoleCode: input.currentRoleCode ?? null,
    expiresAt: input.expiresAt ?? null,
    refreshExpiresAt: input.refreshExpiresAt ?? null,
  });
}

export async function findSessionByAccessToken(accessToken: string) {
  const [row] = await db.select().from(authSessions).where(eq(authSessions.accessToken, accessToken)).limit(1);
  return row ?? null;
}

export async function findSessionByRefreshToken(refreshToken: string) {
  const [row] = await db.select().from(authSessions).where(eq(authSessions.refreshToken, refreshToken)).limit(1);
  return row ?? null;
}

export async function listSessionsByUnionUserId(unionUserId: string) {
  return db.select().from(authSessions).where(eq(authSessions.unionUserId, unionUserId));
}

export async function removeSessionByUnionSceneSpace(unionUserId: string, scene: string, space: string) {
  await db
    .delete(authSessions)
    .where(and(eq(authSessions.unionUserId, unionUserId), eq(authSessions.scene, scene), eq(authSessions.space, space)));
}

export async function removeSessionsByUnionUserId(unionUserId: string) {
  await db.delete(authSessions).where(eq(authSessions.unionUserId, unionUserId));
}

export async function blacklistToken(input: {
  id: string;
  token: string;
  tokenType: "access" | "refresh";
  expiresAt?: Date | null;
}) {
  await db.insert(tokenBlacklists).values({
    id: input.id,
    token: input.token,
    tokenType: input.tokenType,
    expiresAt: input.expiresAt ?? null,
  });
}

export async function isTokenBlacklisted(token: string) {
  const [row] = await db
    .select()
    .from(tokenBlacklists)
    .where(and(eq(tokenBlacklists.token, token), or(isNull(tokenBlacklists.expiresAt), gt(tokenBlacklists.expiresAt, new Date()))))
    .limit(1);
  return Boolean(row);
}
