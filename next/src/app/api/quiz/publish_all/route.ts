import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { publishAllDraftQuizzes } from "@/server/services/quiz-service";

export async function POST() {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    return publishAllDraftQuizzes();
  });
}
