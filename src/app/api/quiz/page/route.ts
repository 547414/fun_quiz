import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { pageQuizzes } from "@/server/services/quiz-service";

export async function POST() {
  return withApi(async () => {
    await requireAuth();
    return pageQuizzes();
  });
}
