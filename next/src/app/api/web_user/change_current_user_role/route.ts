import { z } from "zod";

import { requireAuth } from "@/lib/auth/guard";
import { AppError } from "@/lib/errors";
import { getRefreshTokenCookie, setAccessTokenCookie } from "@/lib/auth/session";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { switchCurrentRole } from "@/server/services/auth-service";

const schema = z.object({
  roleCode: z.string().min(1),
});

export async function POST(request: Request) {
  return withApi(async () => {
    const current = await requireAuth();
    const body = await parseJsonBody(request, schema);
    const refreshToken = await getRefreshTokenCookie(current.space);
    if (!refreshToken) {
      throw new AppError("refresh token missing", 400);
    }
    const result = await switchCurrentRole({
      unionUserId: current.unionUserId,
      roleCode: body.roleCode,
      scene: current.scene,
      space: current.space,
      refreshToken,
    });
    await setAccessTokenCookie(result.accessToken, current.space);
    return result;
  });
}
