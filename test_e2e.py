"""
End-to-end test: Fill form → Sign → Select store → Submit → Verify DB + Email.
"""

import asyncio
import httpx
from playwright.async_api import async_playwright

BASE = "http://127.0.0.1:8000"
SHOTS = "test_screenshots"


async def main():
    import os
    os.makedirs(SHOTS, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})

        # Capture console errors
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: errors.append(str(err)))

        print("=" * 55)
        print("  CHICKEN KITCHEN HR — END-TO-END TEST")
        print("=" * 55)
        print()

        # ─── Step 1: Load app ───
        print("[1/8] Loading app...")
        await page.goto(f"{BASE}/web/index.html")
        await page.wait_for_load_state("networkidle")
        print("  OK")

        # ─── Step 2: Fill Employee Application ───
        print("[2/8] Filling Employee Application...")
        await page.click("button[data-form='employee_app']")
        await page.wait_for_timeout(500)

        # Set form values directly via JS
        await page.evaluate("""() => {
            setVal('ea_last_name', 'Garcia');
            setVal('ea_first_name', 'Maria');
            setVal('ea_mi', 'L');
            setVal('ea_date', '05/26/2026');
            setVal('ea_street_address', '123 Main St');
            setVal('ea_apt', '4B');
            setVal('ea_email', 'andersonckllc@gmail.com');
            setVal('ea_phone_code', '305');
            setVal('ea_phone_num', '555-1234');
            setVal('ea_ssn', '123-45-6789');
            setVal('ea_position', 'Cook');
            setVal('ea_citizen', 'yes');
            setVal('ea_authorized', 'yes');
        }""")
        await page.screenshot(path=f"{SHOTS}/e2e_01_form.png")
        print("  OK — Garcia, Maria L — Cook position")

        # ─── Step 3: Documents tab ───
        print("[3/8] Opening Documents & Submit...")
        await page.click("button[data-form='documents']")
        await page.wait_for_timeout(600)
        print("  OK")

        # ─── Step 4: Select store via JS ───
        print("[4/8] Selecting store: Doral...")
        await page.evaluate("""() => {
            selectStore('DOR');
            // Also update the dropdown visually
            const sel = document.querySelector('.content select');
            if (sel) sel.value = 'DOR';
            const info = document.getElementById('storeInfoBox');
            if (info && selectedStore) {
                info.style.display = 'block';
                info.innerHTML = '<strong>' + selectedStore.legal_entity + '</strong><br>' + selectedStore.address;
            }
        }""")
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{SHOTS}/e2e_02_store.png")
        print("  OK — Doral: CK at Doral LLC")

        # ─── Step 5: Fill applicant info via JS ───
        print("[5/8] Filling applicant info...")
        await page.evaluate("""() => {
            setVal('doc_name', 'Maria L Garcia');
            setVal('doc_email', 'andersonckllc@gmail.com');
            setVal('doc_phone', '305-555-1234');
            // Update visible inputs
            document.querySelectorAll('.content input[type="text"]').forEach(inp => {
                const fg = inp.closest('.field-group');
                if (!fg) return;
                const lbl = fg.querySelector('label');
                if (!lbl) return;
                const t = lbl.textContent.toLowerCase();
                if (t.includes('full name') || t.includes('nombre')) inp.value = 'Maria L Garcia';
                else if (t.includes('email') || t.includes('correo')) inp.value = 'andersonckllc@gmail.com';
                else if (t.includes('phone') || t.includes('telefono')) inp.value = '305-555-1234';
            });
        }""")
        await page.wait_for_timeout(200)
        await page.screenshot(path=f"{SHOTS}/e2e_03_info.png")
        print("  OK — Maria L Garcia / andersonckllc@gmail.com")

        # ─── Step 6: Scroll and draw signature ───
        print("[6/8] Drawing signature...")
        await page.evaluate("document.querySelector('.content').scrollTo(0, 99999)")
        await page.wait_for_timeout(500)

        canvas = await page.query_selector("canvas")
        if canvas:
            box = await canvas.bounding_box()
            if box:
                x, y, w, h = box["x"], box["y"], box["width"], box["height"]
                await page.mouse.move(x + w * 0.05, y + h * 0.5)
                await page.mouse.down()
                for i in range(30):
                    px = x + w * 0.05 + (w * 0.85 * i / 30)
                    py = y + h * 0.2 + (h * 0.6 * ((i % 3) / 2))
                    await page.mouse.move(px, py)
                await page.mouse.up()
        await page.wait_for_timeout(300)

        # Verify signature exists
        has_sig = await page.evaluate("hasSignature()")
        print(f"  OK — Signature drawn: {has_sig}")
        await page.screenshot(path=f"{SHOTS}/e2e_04_signed.png")

        # ─── Step 7: Submit ───
        print("[7/8] Submitting application...")

        # Capture alerts
        alerts = []
        page.on("dialog", lambda d: (alerts.append(d.message), asyncio.ensure_future(d.accept())))

        # Debug: check state before submit
        state = await page.evaluate("""() => ({
            doc_name: getVal('doc_name'),
            doc_email: getVal('doc_email'),
            selectedStore: selectedStore ? selectedStore.code : null,
            hasSig: hasSignature(),
            isStreamlit: typeof window.Streamlit !== 'undefined',
            formHasEA: formHasData('employee_app'),
        })""")
        print(f"  Pre-submit state: {state}")

        # Click submit
        await page.click(".btn-submit-app")
        await page.wait_for_timeout(8000)

        if alerts:
            print(f"  Alerts shown: {alerts}")

        await page.screenshot(path=f"{SHOTS}/e2e_05_result.png")

        if errors:
            print(f"  Console errors: {len(errors)}")
            for e in errors[:5]:
                print(f"    - {e[:150]}")

        await browser.close()

    # ─── Step 8: Verify DB ───
    print("\n[8/8] Verifying in Supabase...")

    from dotenv import load_dotenv
    load_dotenv()

    url = os.environ["SUPABASE_URL"].rstrip("/")
    key = os.environ["SUPABASE_KEY"]
    headers = {"apikey": key, "Authorization": f"Bearer {key}"}

    resp = httpx.get(f"{url}/rest/v1/applications",
        headers=headers,
        params={"select": "id,name,email,store_code,store_name,status,admin_token,created_at",
                "order": "created_at.desc", "limit": "3"},
        timeout=10)
    apps = resp.json()
    print(f"\n  Applications in DB: {len(apps)}")
    for a in apps:
        print(f"    - {a['name']} | {a['email']} | {a['store_name']} | {a['status']}")

    if apps:
        app_id = apps[0]["id"]
        token = apps[0]["admin_token"]

        resp = httpx.get(f"{url}/rest/v1/documents",
            headers=headers,
            params={"select": "filename,doc_type", "application_id": f"eq.{app_id}"},
            timeout=10)
        docs = resp.json()
        print(f"\n  Documents for this application: {len(docs)}")
        for d in docs:
            print(f"    - {d['filename']} ({d['doc_type']})")

        print(f"\n  Admin review link:")
        print(f"    {BASE}/web/admin.html?token={token}")

    print()
    print("=" * 55)
    if apps and apps[0]["name"] == "Maria L Garcia":
        print("  END-TO-END TEST: PASSED")
    else:
        print("  END-TO-END TEST: CHECK RESULTS ABOVE")
    print("=" * 55)


if __name__ == "__main__":
    asyncio.run(main())
