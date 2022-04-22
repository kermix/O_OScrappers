from selenium_driver import Browser

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException

from exceptions.scrapper import SearchInitError

class GoogleScrapper(Browser):
    def __init__(self, lang):
        super().__init__()

        browser = self.browser

        browser.get(f"https://www.google.com?hl={lang}")
        try:
            consent = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@id=\"L2AGLb\"]/div')))
            consent.click()
        except (TimeoutException, KeyError):
            browser.close()
            raise SearchInitError(message = "Cannot initialize search process. Accepting Google's tracking consent failed.")

        self._query = None

    @property
    def browser(self):
        return self.driver

    @property
    def query(self):
        return self._query

    def search(self, query) -> None: 
        browser = self.driver
        
        self._query = query

        try:
            search_input = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//form[@role=\"search\"]//input[@type=\"text\"]')))
            search_input.send_keys(query)
            search_input.submit()
        except TimeoutError:
            raise SearchInitError(message="Cannot initialize search process. Search bar is not clickable.")
        except ElementNotInteractableException:
            raise SearchInitError(message="Cannot initialize search process. Cannot submit or enter your query.")

        



        