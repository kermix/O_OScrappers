from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

class Browser:
    def __init__(self):
        self.__driver = webdriver.Chrome(options=self.__set_chrome_options())

    @property
    def driver(self):
        return self.__driver

    def close(self):
        self.driver.close()

    @staticmethod
    def __set_chrome_options() -> Options:
        """Sets chrome options for Selenium.
        Chrome options for headless browser is enabled.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}

        return chrome_options

    def scroll(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

if __name__ == "__main__":
    driver = Browser().driver
    # Do stuff with your driver
    driver.close()