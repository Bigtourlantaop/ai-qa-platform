from playwright.sync_api import Page, expect
from tests.pages.login_page import LoginPage
from tests.pages.inventory_page import InventoryPage


def test_successful_login(login_page: LoginPage, inventory_page: InventoryPage, page: Page):
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    assert inventory_page.get_title_text() == "Products"


def test_login_with_wrong_password(login_page: LoginPage):
    login_page.login("standard_user", "wrong_password")

    expect(login_page.error_message).to_be_visible()
    assert "do not match" in login_page.get_error_text()


def test_login_with_locked_out_user(login_page: LoginPage):
    login_page.login("locked_out_user", "secret_sauce")

    expect(login_page.error_message).to_be_visible()
    assert "locked out" in login_page.get_error_text()