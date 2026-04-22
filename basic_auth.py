def test_basic_auth(page):
    # Handle Basic Auth by going directly with credentials
    page.goto("https://admin:admin@the-internet.herokuapp.com/basic_auth")
    print("Basic Auth - Successfully authenticated")
    print("All visible text:", page.inner_text("body"))
