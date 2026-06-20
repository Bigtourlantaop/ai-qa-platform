SAUCEDEMO_LOGIN_CONTEXT = """
URL: https://www.saucedemo.com/

Selectors ที่มีอยู่จริงในหน้านี้:
- Username input: page.locator("#user-name")
- Password input: page.locator("#password")
- Login button: page.locator("#login-button")
- Error message: page.locator("[data-test='error']")
- Page title (หลัง login สำเร็จ): page.locator(".title")

URL หลัง login สำเร็จ: https://www.saucedemo.com/inventory.html

Valid test users:
- standard_user / secret_sauce (login สำเร็จ)
- locked_out_user / secret_sauce (ถูก lock บัญชี)
"""