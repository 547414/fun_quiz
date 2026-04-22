import { z } from "zod";

import { setAccessTokenCookie, setRefreshTokenCookie } from "@/lib/auth/session";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";
import { loginWebUser } from "@/server/services/auth-service";

const schema = z.object({
  account: z.string().min(1),
  password: z.string().min(1).default("123456"),
  scene: z.string().default("WEB"),
  space: z.string().default("WEB"),
});

export async function POST(request: Request) {
  return withApi(async () => {
    const body = await parseJsonBody(request, schema);
    const result = await loginWebUser(body);
    await setAccessTokenCookie(result.union_user_info.accessToken, body.space);
    await setRefreshTokenCookie(result.union_user_info.refreshToken, body.space);
    return result;
  });
}
