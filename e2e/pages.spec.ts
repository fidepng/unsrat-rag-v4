import { test, expect } from '@playwright/test';

test.describe('UNSRAT RAG 5 Frontend Pages & UI Hardening E2E', () => {
  test('Page 1: INSPIRE UNSRAT Replica with Onboarding Modal, Topbar CTA, and In-Dashboard Banner', async ({ page }) => {
    const response = await page.goto('/inspire');
    expect(response?.status()).toBe(200);
    await page.waitForLoadState('domcontentloaded');
    await expect(page).toHaveTitle(/Portal INSPIRE/i);

    // 1. Check Onboarding Dialog on initial visit
    const onboardModal = page.locator('#rag-onboard-modal');
    await expect(onboardModal).toBeVisible({ timeout: 5000 });
    const onboardStartBtn = page.locator('#rag-onboard-start-btn');
    await expect(onboardStartBtn).toBeVisible();

    // Dismiss onboarding via Start Button -> Opens Chat Modal
    await onboardStartBtn.click();
    const modal = page.locator('#rag-modal');
    await expect(modal).toBeVisible({ timeout: 10000 });
    await expect(onboardModal).toBeHidden();

    // Close chat modal
    const closeBtn = page.locator('#rag-modal-close');
    await closeBtn.click();
    await expect(modal).toBeHidden();

    // 2. Check Top Notice Bar (Running text marquee)
    const noticeBar = page.locator('.rag-top-notice-bar');
    await expect(noticeBar).toBeVisible();
    await expect(noticeBar.locator('.rag-notice-badge')).toHaveText(/Simulasi Portal/i);
    await expect(noticeBar.locator('.rag-notice-marquee-content')).toBeVisible();

    // 3. Check In-Dashboard Banner inside background iframe (Informational, anonymized)
    const bgFrame = page.frameLocator('#rag-bg-iframe');
    const userName = bgFrame.locator('#inspire-user-name');
    await expect(userName).toHaveText('MAHASISWA SIMULASI UNSRAT');
    const userNim = bgFrame.locator('#inspire-user-nim');
    await expect(userNim).toHaveText('22021106XXXX');
    const warningAlert = bgFrame.locator('#inspire-warning-alert');
    await expect(warningAlert).toBeHidden();

    // 4. Open Chat Widget via Floating Trigger Button
    const triggerBtn = page.locator('#rag-trigger-btn');
    await expect(triggerBtn).toBeVisible();
    await triggerBtn.click();
    await expect(modal).toBeVisible({ timeout: 10000 });

    // 5. Check Chat Interaction & Character Counter
    const charCounter = page.locator('#rag-char-counter');
    await expect(charCounter).toBeVisible({ timeout: 10000 });
    await expect(charCounter).toHaveText('0 / 1000');

    const userInput = page.locator('#rag-user-input');
    await userInput.fill('Berapa batas SKS?');
    await expect(charCounter).toHaveText('17 / 1000');
  });

  test('Page 1 (Demo Mode): INSPIRE UNSRAT with ?demo=1 shows Author Profile', async ({ page }) => {
    const response = await page.goto('/inspire?demo=1');
    expect(response?.status()).toBe(200);
    await page.waitForLoadState('domcontentloaded');

    // Dismiss onboard modal if open to view background
    const exploreBtn = page.locator('#rag-onboard-explore-btn');
    if (await exploreBtn.isVisible()) {
      await exploreBtn.click();
    }

    // Verify Author Profile rendered in background iframe
    const bgFrame = page.frameLocator('#rag-bg-iframe');
    const userName = bgFrame.locator('#inspire-user-name');
    await expect(userName).toHaveText('TEOFIDE W. K. PANGEMANAN');
    const userNim = bgFrame.locator('#inspire-user-nim');
    await expect(userNim).toHaveText('220211060317');
    const warningAlert = bgFrame.locator('#inspire-warning-alert');
    await expect(warningAlert).toBeVisible();
  });

  test('Page 2: UNSRATACID Landing Mock & Chatbot UI with Char Counter', async ({ page }) => {
    const response = await page.goto('/unsratacid');
    expect(response?.status()).toBe(200);
    await expect(page).toHaveTitle(/Universitas Sam Ratulangi/i);

    // Open chat widget
    const triggerBtn = page.locator('#rag-trigger-btn');
    await expect(triggerBtn).toBeVisible();
    await triggerBtn.click();

    // Check modal and character counter
    const modal = page.locator('#rag-modal');
    await expect(modal).toBeVisible({ timeout: 10000 });

    const charCounter = page.locator('#rag-char-counter');
    await expect(charCounter).toBeVisible({ timeout: 10000 });
    await expect(charCounter).toHaveText('0 / 1000');

    // Type in input
    const userInput = page.locator('#rag-user-input');
    await userInput.fill('Syarat cuti kuliah apa saja?');
    await expect(charCounter).toHaveText('28 / 1000');
  });

  test('Page 3: Evaluation Dashboard loads and renders stats', async ({ page }) => {
    const response = await page.goto('/evaluation');
    expect(response?.status()).toBe(200);
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('h1, h2').first()).toBeVisible();
  });

  test('Page 4: Developer Panel loads with Local Dev Direct Access Badge', async ({ page }) => {
    const response = await page.goto('/dev');
    expect(response?.status()).toBe(200);
    await expect(page.locator('h1:has-text("UNSRAT RAG")')).toBeVisible();

    // Check environment badge
    const devEnvBadge = page.locator('#dev-env-badge');
    await expect(devEnvBadge).toBeVisible();
    await expect(devEnvBadge).toHaveText(/Local Dev/i, { timeout: 10000 });
  });

  test('Page 5: Diagnostics & Testing SPA loads with Char Counter', async ({ page }) => {
    const response = await page.goto('/testing');
    expect(response?.status()).toBe(200);
    await expect(page.locator('#tab-chat')).toBeVisible();

    // Check character counter
    const charCounter = page.locator('#char-counter');
    await expect(charCounter).toBeVisible();
    await expect(charCounter).toHaveText('0 / 1000');

    // Type in textarea
    const userInput = page.locator('#user-input');
    await userInput.fill('KRS online kapan dibuka?');
    await expect(charCounter).toHaveText('24 / 1000');
  });
});

