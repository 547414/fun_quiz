import { headers } from "next/headers";
import { refreshRequestSchema } from "@/contracts/auth";
import { AppError } from "@/lib/errors";
import { getRefreshTokenCookie, setAccessTokenCookie, setRefreshTokenCookie } from "@/lib/auth/session";
import { withApi } from "@/lib/http";
import { parseJsonBodyOrDefault } from "@/lib/request";
import { refreshAccessToken } from "@/server/services/auth-service";

export async function POST(request: Request) {
  return withApi(async () => {
    const headerStore = await headers();
    const scene = headerStore.get("scene") ?? "WEB";
    const space = headerStore.get("space") ?? "WEB";
    const body = await parseJsonBodyOrDefault(request, refreshRequestSchema.partial(), { refreshToken: undefined });
    const refreshToken = body.refreshToken ?? (await getRefreshTokenCookie(space));
    if (!refreshToken) {
      throw new AppError("refreshToken is required", 400);
    }
    const result = await refreshAccessToken({
      refreshToken,
      scene,
      space,
    });
    await setAccessTokenCookie(result.accessToken, space);
    await setRefreshTokenCookie(result.refreshToken, space);
    return result;
  });
}
