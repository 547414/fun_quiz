import { expect, test } from "@playwright/test";

test("h5 entry shows hint when token missing", async ({ page }) => {
  await page.goto("/quiz");
  await expect(page.getByText("缺少 token 参数")).toBeVisible();
});

test("h5 entry handles invalid token without crashing", async ({ page }) => {
  await page.goto("/quiz?token=demo");
  await expect(page.getByText("请求参数错误")).toHaveCount(0);
  await expect(page.getByText("暂无历史结果")).toBeVisible();
});
