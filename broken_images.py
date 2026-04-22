def test_broken_images(page):
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
