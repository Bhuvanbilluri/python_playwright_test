from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Open browser
    page = browser.new_page()
    
    page.goto("https://the-internet.herokuapp.com/")
    print(page.title())  # Print page title
    
    page.locator("text=A/B Testing").click()
    print("A/B Testing")
    page.go_back(wait_until="load")

    page.locator("text=Add/Remove Elements").click()
    print("Add/Remove Elements")

    for i in range(5):
        page.locator("text=Add Element").click()
        print("Add Element")


    for i in range(5):
        page.locator("text=Delete").first.click()
        print("Delete")
        
    page.go_back(wait_until="load")

    # Handle Basic Auth by going directly with credentials
    page.goto("https://admin:admin@the-internet.herokuapp.com/basic_auth")
    print("Basic Auth - Successfully authenticated")
 
    # print("Basic Auth - Page title:", page.title())
    
    # # Print various page data
    # print("Current URL:", page.url)
    # print("Page content (first 200 chars):", page.content()[:200])
    # print("Page text (first 200 chars):", page.text_content("body")[:200])
    
    # Get all visible text
    print("All visible text:", page.inner_text("body"))

    page.go_back(wait_until="load")

    page.locator("text=broken images").click()
    print("Broken Images")

    # Check for broken images
    images = page.query_selector_all("img")
    for i, img in enumerate(images):
        src = img.get_attribute("src")
        # Use evaluate to access DOM properties like naturalWidth and naturalHeight
        is_broken = page.evaluate("(img) => img.naturalWidth === 0 || img.naturalHeight === 0", img)
        if is_broken:
            print(f"Image {i+1} (src: {src}) is broken.")
        else:
            print(f"Image {i+1} (src: {src}) is not broken.")

    

    
    page.go_back(wait_until="load")
    
    browser.close()