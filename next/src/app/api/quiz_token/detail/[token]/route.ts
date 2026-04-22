import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { getQuizTokenDetail } from "@/server/services/quiz-service";

type Props = {
  params: Promise<{ token: string }>;
};

export async function POST(_: Request, props: Props) {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    const { token } = await props.params;
    return getQuizTokenDetail(token);
  });
}
