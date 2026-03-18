import { test, expect } from '@playwright/test';

test.describe('InsurerDashboard', () => {
  test('renders sample policy rows', async ({ page }) => {
    await page.goto('/components/InsurerDashboard');
    await page.evaluate(() => {
      document.body.innerHTML = `
        <div id="app"></div>
        <script type="module">
          import React from 'react';
          import ReactDOM from 'react-dom';
          import InsurerDashboard from '/src/components/InsurerDashboard.tsx';
          ReactDOM.createRoot(document.getElementById('app')).render(
            <React.StrictMode>
              <InsurerDashboard />
            </React.StrictMode>
          );
        </script>
      `;
    });

    await page.waitForSelector('table', { timeout: 5000 });

    const rows = page.locator('tbody tr');
    await expect(rows).toHaveCount(2);

    const defaulterRow = page.locator('tr[style*="color: red"]');
    await expect(defaulterRow).toBeVisible();
  });

  test('refresh button triggers new API call', async ({ page }) => {
    let callCount = 0;
    await page.route('**/api/v1/policies', async (route) => {
      callCount++;
      await route.fulfill({
        status: 200,
        body: JSON.stringify([
          {
            "policy_id": 1,
            "policy_type": "AUTO",
            "status": "ACTIVE",
            "next_premium_date": "2024-12-01",
            "amount_due": 500,
            "is_lapsed": false
          }
        ])
      });
    });

    await page.goto('/components/InsurerDashboard');

    const refreshButton = page.locator('button:has-text("Refresh")');
    await refreshButton.click();

    await expect(async () => {
      expect(callCount).toBeGreaterThanOrEqual(2);
    }).toPass();
  });
});
