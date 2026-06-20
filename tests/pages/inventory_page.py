from playwright.sync_api import Page


class InventoryPage:
    """Page Object สำหรับหน้า Inventory (หลัง login สำเร็จ)"""

    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator(".title")

    def get_title_text(self) -> str:
        return self.title.text_content()