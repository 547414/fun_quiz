import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { detailQuiz } from "@/server/services/quiz-service";

type Props = {
  params: Promise<{ quizId: string }>;
};

export async function POST(_: Request, props: Props) {
  return withApi(async () => {
    await requireAuth();
    const { quizId } = await props.params;
    return detailQuiz(quizId);
  });
}
