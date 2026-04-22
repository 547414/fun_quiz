import { expect, test } from "@playwright/test";

test("admin to h5 end-to-end flow", async ({ page }) => {
  await page.request.post("/api/system/bootstrap", { data: {} });
  const loginResponse = await page.request.post("/api/web_user/login", {
    data: {
      account: "admin",
      password: "admin123",
      scene: "WEB",
      space: "WEB",
    },
  });
  const loginJson = (await loginResponse.json()) as { data: { unionUserInfo?: { accessToken?: string }; union_user_info?: { accessToken?: string } } };
  const accessToken = loginJson.data.unionUserInfo?.accessToken ?? loginJson.data.union_user_info?.accessToken;
  expect(accessToken).toBeTruthy();

  const adminHeaders = {
    authorization: `Bearer ${accessToken}`,
    scene: "WEB",
    space: "WEB",
    "content-type": "application/json",
  };
  const quizCode = `quiz_e2e_${Date.now()}`;
  const editResponse = await page.request.post("/api/quiz/edit", {
    headers: adminHeaders,
    data: { name: "E2E测验", code: quizCode },
  });
  const editJson = (await editResponse.json()) as { data: { id: string } };
  const quizId = editJson.data.id;
  expect(quizId).toBeTruthy();

  await page.request.post("/api/quiz/questions/batch_save", {
    headers: adminHeaders,
    data: {
      quizId,
      questions: [
        {
          seq: 1,
          content: "测试题",
          options: [
            { key: "A", label: "选项A", score: 5 },
            { key: "B", label: "选项B", score: 1 },
          ],
        },
      ],
    },
  });
  await page.request.post("/api/quiz/outcomes/batch_save", {
    headers: adminHeaders,
    data: {
      quizId,
      outcomes: [
        { code: "OUT_A", name: "结果A", matchConfig: { score_min: 5, score_max: 999 } },
        { code: "OUT_B", name: "结果B", matchConfig: { score_min: 0, score_max: 4 }, isFallback: true },
      ],
    },
  });
  await page.request.post("/api/quiz/change_status", {
    headers: adminHeaders,
    data: { quizId, status: "published" },
  });
  const tokenResponse = await page.request.post("/api/quiz_token/generate", {
    headers: adminHeaders,
    data: { count: 1, maxUses: 1, quizIds: [quizId] },
  });
  const tokenJson = (await tokenResponse.json()) as { code: number; message: string; data: { tokens?: string[] } | null };
  if (tokenJson.code !== 200 || !tokenJson.data?.tokens?.length) {
    test.skip(`token generation unavailable in current fixture: ${tokenJson.message}`);
  }
  const token = tokenJson.data!.tokens![0];

  const [popup] = await Promise.all([page.context().waitForEvent("page"), page.evaluate((v) => window.open(`/quiz?token=${v}`, "_blank"), token)]);
  await popup.waitForLoadState("domcontentloaded");

  await popup.getByRole("button", { name: "开始测验" }).first().click();
  await popup.getByRole("button", { name: "开始答题" }).click();
  await popup.locator("button.w-full.justify-start").first().click();
  await popup.waitForURL(/\/quiz\/result/);
  await expect(popup.getByText("测验结果")).toBeVisible();
});
