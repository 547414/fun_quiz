import { headers } from "next/headers";

import { requireAuth } from "@/lib/auth/guard";
import { clearAuthCookies, getAccessTokenCookie, getRefreshTokenCookie } from "@/lib/auth/session";
import { withApi } from "@/lib/http";
import { logoutUser } from "@/server/services/auth-service";

export async function POST() {
  return withApi(async () => {
    const current = await requireAuth();
    const headerStore = await headers();
    const scene = headerStore.get("scene") ?? "WEB";
    const space = headerStore.get("space") ?? "WEB";
    const accessToken = await getAccessTokenCookie(space);
    const refreshToken = await getRefreshTokenCookie(space);
    await logoutUser({
      unionUserId: current.unionUserId,
      scene,
      space,
      accessToken,
      refreshToken,
    });
    await clearAuthCookies(space);
    return { success: true };
  });
}
