from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Scraper(webdriver.Chrome):
    def __init__(self) -> None:
        super().__init__()
        self.switch_categories: list[str] = []
        self.subpages: list[str] = []

    def navigate_to(self, url: str) -> None:
        if self.current_url == url:
            pass
        else:
            self.get(url)

    def locate_one(self, xpath: str, timeout: float = 1.0) -> WebElement:
        locator = (By.XPATH, xpath)
        return WebDriverWait(self, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def locate_multiple(self, xpath: str, timeout: float = 5.0) -> list[WebElement]:
        locator = (By.XPATH, xpath)
        return WebDriverWait(self, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )
