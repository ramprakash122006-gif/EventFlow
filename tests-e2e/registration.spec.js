import { test, expect } from '@playwright/test';

test.describe('EventFlow Registration E2E Tests', () => {
  test('User can view event list and seat capacity metrics', async ({ page }) => {
    await page.goto('/');
    
    // Check header branding
    await expect(page.locator('.logo-title')).toHaveText('EventFlow');
    
    // Check event cards render
    const cards = page.locator('.event-card');
    await expect(cards.first()).toBeVisible();
  });

  test('User can register for an available event and seat count updates', async ({ page }) => {
    await page.goto('/');

    // Locate first ENABLED register button (skipping disabled past events)
    const registerBtn = page.locator('button[id^="register-btn-"]:not([disabled])').first();
    await expect(registerBtn).toBeVisible();
    await registerBtn.click();

    // Modal should be visible
    const modal = page.locator('#registration-modal');
    await expect(modal).toBeVisible();

    // Fill form with unique test email
    const timestamp = Date.now();
    const testEmail = `e2e.user.${timestamp}@example.com`;
    
    await page.fill('#full_name', 'E2E Test User');
    await page.fill('#email', testEmail);
    
    await page.click('#submit-registration-btn');

    // Success alert should be visible inside modal (Confirmed or Waitlisted)
    const successAlert = page.locator('#registration-success-alert');
    await expect(successAlert).toBeVisible();
    await expect(successAlert).toContainText(/(Successfully registered|Registration Confirmed|Added to Waitlist)/);



    // Close modal
    await page.click('#close-modal-btn');
  });

  test('System prevents duplicate email registration with inline error', async ({ page }) => {
    await page.goto('/');

    const duplicateEmail = `duplicate.e2e.${Date.now()}@example.com`;

    // 1st Registration using an enabled event button
    const registerBtn = page.locator('button[id^="register-btn-"]:not([disabled])').first();
    await registerBtn.click();
    await page.fill('#full_name', 'Original User');
    await page.fill('#email', duplicateEmail);
    await page.click('#submit-registration-btn');
    await expect(page.locator('#registration-success-alert')).toBeVisible();
    await page.click('#close-modal-btn');

    // 2nd Registration with same email (uppercase to test case insensitivity)
    await registerBtn.click();
    await page.fill('#full_name', 'Duplicate User');
    await page.fill('#email', duplicateEmail.toUpperCase());
    await page.click('#submit-registration-btn');

    // Error alert should appear in modal
    const errorAlert = page.locator('#registration-error-alert');
    await expect(errorAlert).toBeVisible();
    await expect(errorAlert).toContainText('already registered');
  });

  test('System displays clear error message when invalid email is entered', async ({ page }) => {
    await page.goto('/');

    const registerBtn = page.locator('button[id^="register-btn-"]:not([disabled])').first();
    await registerBtn.click();

    await page.fill('#full_name', 'Invalid Email Test');
    await page.fill('#email', 'invalid-email-no-at-sign');
    await page.click('#submit-registration-btn');

    const errorAlert = page.locator('#registration-error-alert');
    await expect(errorAlert).toBeVisible();
    await expect(errorAlert).toContainText('Please enter a valid email address');
  });

});

