import { cookies } from "next/headers";

const IS_PRODUCTION = process.env.NODE_ENV === "production";

function normalizeSpace(space?: string) {
  return (space ?? "WEB").trim().toLowerCase();
}

function getAccessCookieName(space?: string) {
  return `fq_access_token_${normalizeSpace(space)}`;
}

function getRefreshCookieName(space?: string) {
  return `fq_refresh_token_${normalizeSpace(space)}`;
}

export async function setAccessTokenCookie(token: string, space?: string) {
  const cookieStore = await cookies();
  cookieStore.set(getAccessCookieName(space), token, {
    httpOnly: true,
    secure: IS_PRODUCTION,
    sameSite: "lax",
    path: "/",
  });
}

export async function setRefreshTokenCookie(token: string, space?: string) {
  const cookieStore = await cookies();
  cookieStore.set(getRefreshCookieName(space), token, {
    httpOnly: true,
    secure: IS_PRODUCTION,
    sameSite: "lax",
    path: "/",
  });
}

export async function clearAccessTokenCookie(space?: string) {
  const cookieStore = await cookies();
  cookieStore.delete(getAccessCookieName(space));
}

export async function clearRefreshTokenCookie(space?: string) {
  const cookieStore = await cookies();
  cookieStore.delete(getRefreshCookieName(space));
}

export async function clearAuthCookies(space?: string) {
  await clearAccessTokenCookie(space);
  await clearRefreshTokenCookie(space);
}

export async function getAccessTokenCookie(space?: string) {
  const cookieStore = await cookies();
  const current = cookieStore.get(getAccessCookieName(space))?.value;
  if (current) return current;
  return cookieStore.get("fq_access_token")?.value;
}

export async function getRefreshTokenCookie(space?: string) {
  const cookieStore = await cookies();
  const current = cookieStore.get(getRefreshCookieName(space))?.value;
  if (current) return current;
  return cookieStore.get("fq_refresh_token")?.value;
}
