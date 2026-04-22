import { loginRequestSchema } from "@/contracts/auth";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { setAccessTokenCookie, setRefreshTokenCookie } from "@/lib/auth/session";
import { loginWebUser } from "@/server/services/auth-service";

export async function POST(request: Request) {
  return withApi(async () => {
    const body = await parseJsonBody(request, loginRequestSchema);
    const result = await loginWebUser(body);
    await setAccessTokenCookie(result.union_user_info.accessToken, body.space);
    await setRefreshTokenCookie(result.union_user_info.refreshToken, body.space);
    return result;
  });
}
