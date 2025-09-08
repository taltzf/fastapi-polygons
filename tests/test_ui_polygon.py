import pytest
from playwright.sync_api import sync_playwright
import requests
import time

BASE_URL = "http://127.0.0.1:8000"
POLYGONS = [
    {"name": "Polygon1", "points": [(50,50),(200,50),(200,200),(50,200)]},
    {"name": "Polygon2", "points": [(300,100),(450,100),(450,250),(300,250)]},
]

# -------------------------------
# Helper functions
# -------------------------------

def cleanup_polygons():
    """Delete all test polygons via API."""
    try:
        polygons = requests.get(f"{BASE_URL}/api/polygons/").json()
        for p in polygons:
            if p["name"] in [poly["name"] for poly in POLYGONS]:
                requests.delete(f"{BASE_URL}/api/polygon/{p['id']}")
    except Exception as e:
        print(f"Cleanup failed: {e}")

# -------------------------------
# Test
# -------------------------------

@pytest.mark.ui
def test_ui_multiple_polygons():
    # Cleanup before test
    cleanup_polygons()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(BASE_URL + "/", wait_until="networkidle")

        # Wait for canvas
        canvas = page.wait_for_selector("#canvas", timeout=5000)
        box = canvas.bounding_box()
        assert box is not None, "Canvas bounding box not found"

        for poly in POLYGONS:
            # Draw polygon points
            for x_offset, y_offset in poly["points"]:
                page.mouse.click(box["x"] + x_offset, box["y"] + y_offset)

            # Handle JS prompt
            page.once("dialog", lambda dialog, name=poly["name"]: dialog.accept(name))

            # Click Finish Polygon
            page.locator("#finishPolygon").click()

            # Wait for polygon to appear
            polygon_locator = page.locator(f".polygon-item:has-text('{poly['name']}')").first
            polygon_locator.wait_for(timeout=5000)
            assert polygon_locator is not None

        # Verify all polygons exist in the list
        polygon_items = page.locator(".polygon-item").element_handles()
        names = [item.inner_text() for item in polygon_items]
        for poly in POLYGONS:
            assert any(poly["name"] in name for name in names)

        # Delete all polygons
        for poly in POLYGONS:
            page.locator(f".polygon-item:has-text('{poly['name']}') button").first.click()
            time.sleep(0.2)  # wait for UI update

        # Verify all polygons deleted
        remaining_items = page.locator(".polygon-item").element_handles()
        remaining_names = [item.inner_text() for item in remaining_items]
        for poly in POLYGONS:
            assert all(poly["name"] not in name for name in remaining_names)

        browser.close()

    # Cleanup just in case
    cleanup_polygons()
