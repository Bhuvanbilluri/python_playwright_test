def test_add_remove_elements(page):
    page.locator("text=Add/Remove Elements").click()
    print("Add/Remove Elements")

    # Add 5 elements
    for i in range(5):
        page.locator("text=Add Element").click()
        print("Add Element")

    # Delete 5 elements
    for i in range(5):
        page.locator("text=Delete").first.click()
        print("Delete")
