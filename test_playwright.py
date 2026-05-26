"""
Playwright visual test for Chicken Kitchen HR Forms.
Captures screenshots of: store selection, forms, signature pad, admin page.
"""

import asyncio
from playwright.async_api import async_playwright

BASE = "http://127.0.0.1:8000"
SHOTS_DIR = "test_screenshots"


async def main():
    import os
    os.makedirs(SHOTS_DIR, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})

        # 1. Landing page
        print("[1/7] Loading landing page...")
        await page.goto(BASE)
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=f"{SHOTS_DIR}/01_landing.png", full_page=True)
        print("  -> Screenshot: 01_landing.png")

        # 2. Employee Application form
        print("[2/7] Opening Employee Application...")
        await page.click("button[data-form='employee_app']")
        await page.wait_for_timeout(500)
        await page.screenshot(path=f"{SHOTS_DIR}/02_employee_app.png", full_page=True)
        print("  -> Screenshot: 02_employee_app.png")

        # 3. Fill some fields
        print("[3/7] Filling Employee Application fields...")
        inputs = await page.query_selector_all(".content input[type='text']")
        if len(inputs) >= 4:
            await inputs[0].fill("Zamora")       # Last name
            await inputs[1].fill("Monica")        # First name
            await inputs[2].fill("")              # MI
            await inputs[3].fill("05/26/2026")    # Date
        await page.screenshot(path=f"{SHOTS_DIR}/03_form_filled.png", full_page=True)
        print("  -> Screenshot: 03_form_filled.png")

        # 4. Documents & Submit tab (store selection + signature)
        print("[4/7] Opening Documents & Submit...")
        await page.click("button[data-form='documents']")
        await page.wait_for_timeout(800)
        await page.screenshot(path=f"{SHOTS_DIR}/04_documents_store.png", full_page=True)
        print("  -> Screenshot: 04_documents_store.png")

        # 5. Select a store
        print("[5/7] Selecting store 'Doral'...")
        store_select = await page.query_selector(".content select")
        if store_select:
            await store_select.select_option("DOR")
            await page.wait_for_timeout(300)
        await page.screenshot(path=f"{SHOTS_DIR}/05_store_selected.png", full_page=True)
        print("  -> Screenshot: 05_store_selected.png")

        # 6. Draw signature on canvas
        print("[6/7] Drawing signature on canvas...")
        canvas = await page.query_selector("canvas")
        if canvas:
            box = await canvas.bounding_box()
            if box:
                x, y = box["x"], box["y"]
                w, h = box["width"], box["height"]
                # Draw a simple squiggle
                await page.mouse.move(x + w * 0.1, y + h * 0.5)
                await page.mouse.down()
                for i in range(20):
                    await page.mouse.move(
                        x + w * 0.1 + (w * 0.7 * i / 20),
                        y + h * 0.3 + (h * 0.4 * (i % 2)),
                    )
                await page.mouse.up()
                await page.wait_for_timeout(200)
        await page.screenshot(path=f"{SHOTS_DIR}/06_signature_drawn.png", full_page=True)
        print("  -> Screenshot: 06_signature_drawn.png")

        # 7. Admin review page
        print("[7/7] Loading admin review page...")
        await page.goto(f"{BASE}/web/admin.html?token=test-token-123")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=f"{SHOTS_DIR}/07_admin_page.png", full_page=True)
        print("  -> Screenshot: 07_admin_page.png")

        # 8. Check store API
        print("\n[API] Testing /api/stores endpoint...")
        resp = await page.goto(f"{BASE}/api/stores")
        if resp:
            body = await resp.text()
            count = body.count('"code"')
            print(f"  -> /api/stores returned {count} stores")

        # 9. Check store detail API
        resp = await page.goto(f"{BASE}/api/store/DOR")
        if resp:
            body = await resp.text()
            print(f"  -> /api/store/DOR: {body[:120]}")

        await browser.close()

    print(f"\nDone! {len(os.listdir(SHOTS_DIR))} screenshots saved in {SHOTS_DIR}/")


if __name__ == "__main__":
    asyncio.run(main())
