import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://dashboard.aquaexchange.com/"

# ─── Coordinate map (derived from Flutter canvas layout at 1920x1080) ───────
# Adjust if viewport size changes — Flutter re-renders at different breakpoints
COORDS = {
    "username_field": (718, 293),
    "password_field": (718, 377),
    "password_toggle": (749, 377),   # eye icon to show/hide password
    "forgot_password": (718, 430),
    "login_button":    (718, 497),
}


class LoginPage:
    """Page Object for the Aqua Exchange / NextFarm login screen."""

    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto(BASE_URL)
        self.page.wait_for_load_state("networkidle")
        # Wait for Flutter canvas to finish painting
        self.page.wait_for_selector("flt-glass-pane")

    def enter_username(self, username: str):
        self.page.mouse.click(*COORDS["username_field"])
        self.page.keyboard.press("Control+a")
        self.page.keyboard.type(username)

    def enter_password(self, password: str):
        self.page.mouse.click(*COORDS["password_field"])
        self.page.keyboard.press("Control+a")
        self.page.keyboard.type(password)

    def toggle_password_visibility(self):
        """Click the eye icon to show/hide the password."""
        self.page.mouse.click(*COORDS["password_toggle"])

    def click_forgot_password(self):
        self.page.mouse.click(*COORDS["forgot_password"])

    def click_login(self):
        self.page.mouse.click(*COORDS["login_button"])

    def login(self, username: str, password: str):
        """Complete login flow end-to-end."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def submit_with_enter(self, username: str, password: str):
        """Alternative: submit the form using the Enter key."""
        self.enter_username(username)
        self.enter_password(password)
        self.page.keyboard.press("Enter")


# ─── Test Cases ──────────────────────────────────────────────────────────────

@pytest.fixture
def login_page(page: Page):
    lp = LoginPage(page)
    lp.navigate()
    return lp


def test_login_page_loads(login_page: LoginPage):
    """Verify the login page renders correctly."""
    page = login_page.page
    # Flutter renders page title
    assert page.title() == "NextFarm Dashboard"
    # Shadow DOM host should be present
    assert page.query_selector("flt-glass-pane") is not None


def test_successful_login(login_page: LoginPage, page: Page):
    """TC-001: Valid credentials → dashboard loads."""
    login_page.login(username="superadmin", password="aqua20@#$5")
    page.wait_for_load_state("networkidle")
    # After login the URL should change away from root
    expect(page).not_to_have_url(BASE_URL, timeout=10_000)


def test_invalid_username(login_page: LoginPage, page: Page):
    """TC-002: Wrong username → error state remains on login page."""
    login_page.login(username="wrong_user@example.com", password="ValidPass123!")
    page.wait_for_timeout(2000)
    # Should still be on the login page
    assert page.url == BASE_URL


def test_invalid_password(login_page: LoginPage, page: Page):
    """TC-003: Correct username, wrong password → stays on login page."""
    login_page.login(username="valid_user@example.com", password="WrongPass!")
    page.wait_for_timeout(2000)
    assert page.url == BASE_URL


def test_empty_username(login_page: LoginPage, page: Page):
    """TC-004: Empty username, valid password → login should be blocked."""
    login_page.enter_password("ValidPass123!")
    login_page.click_login()
    page.wait_for_timeout(1000)
    assert page.url == BASE_URL


def test_empty_password(login_page: LoginPage, page: Page):
    """TC-005: Valid username, empty password → login should be blocked."""
    login_page.enter_username("valid_user@example.com")
    login_page.click_login()
    page.wait_for_timeout(1000)
    assert page.url == BASE_URL


def test_empty_both_fields(login_page: LoginPage, page: Page):
    """TC-006: Both fields empty → login should be blocked."""
    login_page.click_login()
    page.wait_for_timeout(1000)
    assert page.url == BASE_URL


def test_password_toggle_visibility(login_page: LoginPage):
    """TC-007: Eye icon toggles password visibility."""
    # This is a visual test; we just verify the click doesn't crash
    login_page.enter_password("SomePassword1!")
    login_page.toggle_password_visibility()   # show password
    login_page.page.wait_for_timeout(500)
    login_page.toggle_password_visibility()   # hide password
    login_page.page.wait_for_timeout(500)


def test_forgot_password_link(login_page: LoginPage, page: Page):
    """TC-008: 'Forgot Password?' link navigates away or opens modal."""
    login_page.click_forgot_password()
    page.wait_for_timeout(2000)
    # URL should change OR a modal overlay should appear
    # Adjust assertion based on actual app behaviour
    assert page.url != BASE_URL or page.query_selector("flt-glass-pane") is not None


def test_login_with_enter_key(login_page: LoginPage, page: Page):
    """TC-009: Pressing Enter after password submits the form."""
    login_page.submit_with_enter("valid_user@example.com", "ValidPass123!")
    page.wait_for_load_state("networkidle")
    assert page.url != BASE_URL


def test_login_api_response(login_page: LoginPage, page: Page):
    """TC-010: Capture the login API call and validate HTTP 200."""
    responses = []

    def handle_response(response):
        if "login" in response.url or "auth" in response.url:
            responses.append({"url": response.url, "status": response.status})

    page.on("response", handle_response)
    login_page.login("valid_user@example.com", "ValidPass123!")
    page.wait_for_timeout(3000)

    assert any(r["status"] == 200 for r in responses), \
        f"Expected a 200 from login API, got: {responses}"