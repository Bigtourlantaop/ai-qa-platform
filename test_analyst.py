import os
from dotenv import load_dotenv
from src.ai_engine.failure_analyst import FailureAnalyst

load_dotenv()

analyst = FailureAnalyst()

# เคส TC-001 จากวันนี้ - AI ใช้ lambda ผิด API
test_code = """
def test_add_to_cart_and_checkout_success(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    page.locator(".inventory_item_name").first.click()
    expect(page).to_have_url(lambda url: "inventory-item.html" in url)
"""

error_message = """
playwright._impl._errors.Error: value must be a string or regular expression
"""

result = analyst.analyze(test_code, error_message)

print(f"Category: {result.root_cause_category}")
print(f"Confidence: {result.confidence}")
print(f"Explanation: {result.explanation}")
print(f"Suggested Fix: {result.suggested_fix}")