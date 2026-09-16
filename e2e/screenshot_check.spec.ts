import { test, expect } from '@playwright/test';

test.describe('Visual Screenshot Verification for Chat Input & Counter', () => {
  test('Capture INSPIRE Chat Form', async ({ page }) => {
    await page.goto('/inspire');
    const onboardStartBtn = page.locator('#rag-onboard-start-btn');
    if (await onboardStartBtn.isVisible()) {
      await onboardStartBtn.click();
    } else {
      await page.click('#rag-trigger-btn');
    }
    await page.waitForSelector('#rag-modal', { state: 'visible' });
    const chatForm = page.locator('#rag-chat-form');
    await chatForm.screenshot({ path: 'e2e/screenshots/inspire_input_empty.png' });

    // Type text
    await page.fill('#rag-user-input', 'Bagaimana prosedur pengisian KRS di UNSRAT untuk semester genap?');
    await chatForm.screenshot({ path: 'e2e/screenshots/inspire_input_typed.png' });
  });

  test('Capture UNSRATACID Chat Form', async ({ page }) => {
    await page.goto('/unsratacid');
    await page.click('#rag-trigger-btn');
    await page.waitForSelector('#rag-modal', { state: 'visible' });
    const chatForm = page.locator('#rag-chat-form');
    await chatForm.screenshot({ path: 'e2e/screenshots/unsratacid_input_empty.png' });

    // Type text
    await page.fill('#rag-user-input', 'Bagaimana syarat dan batas waktu cuti akademik?');
    await chatForm.screenshot({ path: 'e2e/screenshots/unsratacid_input_typed.png' });
  });

  test('Capture INSPIRE First-Visit Onboarding Modal', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto('/inspire');
    await page.waitForSelector('#rag-onboard-modal', { state: 'visible' });
    await page.screenshot({ path: 'e2e/screenshots/inspire_onboard_modal.png' });
  });

  test('Capture INSPIRE Full View with Notice Bar & In-Dashboard Banner (Simulation Mode)', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto('/inspire');
    const exploreBtn = page.locator('#rag-onboard-explore-btn');
    if (await exploreBtn.isVisible()) {
      await exploreBtn.click();
    }
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'e2e/screenshots/inspire_full_simulation.png' });
  });

  test('Capture INSPIRE Full View (Demo Mode ?demo=1)', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto('/inspire?demo=1');
    const exploreBtn = page.locator('#rag-onboard-explore-btn');
    if (await exploreBtn.isVisible()) {
      await exploreBtn.click();
    }
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'e2e/screenshots/inspire_full_demo.png' });
  });

  test('Capture INSPIRE Mobile View (390x844)', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto('/inspire');
    const exploreBtn = page.locator('#rag-onboard-explore-btn');
    if (await exploreBtn.isVisible()) {
      await exploreBtn.click();
    }
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'e2e/screenshots/inspire_mobile_simulation.png' });
  });
});
