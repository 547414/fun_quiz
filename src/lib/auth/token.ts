import { SignJWT, jwtVerify } from "jose";

import { env } from "@/lib/env";
import { parseExpiresInToSeconds } from "@/lib/time";

export type JwtPayload = {
  unionUserId: string;
  webUserId: string;
  account: string;
  roleCodes: string[];
  currentRoleCode?: string;
  scene: string;
  space: string;
};

const secret = new TextEncoder().encode(env.APP_JWT_SECRET);

export async function signAccessToken(payload: JwtPayload) {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime(env.APP_JWT_EXPIRES_IN)
    .sign(secret);
}

export async function signRefreshToken(payload: JwtPayload) {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime("7d")
    .sign(secret);
}

export async function verifyAccessToken(token: string): Promise<JwtPayload> {
  const result = await jwtVerify(token, secret);
  return result.payload as JwtPayload;
}

export async function verifyRefreshToken(token: string): Promise<JwtPayload> {
  const result = await jwtVerify(token, secret);
  return result.payload as JwtPayload;
}

export function getAccessTokenExpiresAt() {
  return new Date(Date.now() + parseExpiresInToSeconds(env.APP_JWT_EXPIRES_IN) * 1000);
}

export function getRefreshTokenExpiresAt() {
  return new Date(Date.now() + 7 * 24 * 3600 * 1000);
}
