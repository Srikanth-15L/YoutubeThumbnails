import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 800})
    
    file_url = "file:///c:/Users/vasup/OneDrive/Desktop/Srikanth_2026/youtube_thumbnailer/custom_diagram.html"
    page.goto(file_url)
    
    # Wait for Mermaid to initialize and render
    time.sleep(3)
    
    # Take screenshot of the Mermaid div specifically, or the whole page
    element = page.locator(".mermaid")
    if element.is_visible():
        element.screenshot(path="architecture.png")
    else:
        page.screenshot(path="architecture.png", full_page=True)
        
    print("Screenshot saved to architecture.png")
    browser.close()
