from playwright.sync_api import Page


class LoginPage:
    """Page Object สำหรับหน้า Login ของ SauceDemo"""

    def __init__(self, page: Page):
        self.page = page
        self.url = "https://www.saucedemo.com/"

        # Locators
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")

    def goto(self):
        self.page.goto(self.url)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_text(self) -> str:
        return self.error_message.text_content()