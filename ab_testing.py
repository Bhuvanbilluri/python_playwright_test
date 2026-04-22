def test_ab_testing(page):
    page.goto("https://the-internet.herokuapp.com/")
    page.locator("text=A/B Testing").click()
    print("A/B Testing")
    print("Page title:", page.title())
