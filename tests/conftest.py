import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page
from tests.pages.login_page import LoginPage
from tests.pages.inventory_page import InventoryPage

load_dotenv()


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    lp = LoginPage(page)
    lp.goto()
    return lp


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    lp = LoginPage(page)
    lp.goto()
    lp.login("standard_user", "secret_sauce")
    return page