from misc.queue import Queue
from scrappers.google_scrapper import GoogleScrapper

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from exceptions.scrapper import NoResultError, ElementIsNotPaaQuestionError


class PaaSearch(GoogleScrapper):
    def __init__(self, lang):
        super().__init__(lang)

        self._paa_block = None

    @property
    def paa_block(self):
        return self._paa_block

    def search(self, query) -> None:
        browser = self.driver

        super().search(query)

        try:
            paa_block = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//div[@data-initq=\"{query}\"]")))
        except:
            raise NoResultError("No PAA block found.")

        self._paa_block = paa_block

    def expand(self, depth=1):
        browser = self.driver
        paa_block = self.paa_block

        self.scroll(paa_block)

        while(depth):
            questions_queue = Queue()
            for q in self.__get_questions_tags():
                question = self.Question(q)
                questions_queue.enqueue(question)

            while(not questions_queue.isEmpty()):
                try:
                    question = questions_queue.front()
                    q = question.question
                except ElementIsNotPaaQuestionError:
                    questions_queue.dequeue()
                    continue

                questions_queue.dequeue()
                self.scroll(q)
                q.click()
                q_label = q.get_attribute('aria-controls')

                try:
                    answer = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, f"//div[contains(@class, 'related-question-pair')]//div[@id=\"{q_label}\"]")))
                except TimeoutError:
                    questions_queue.enqueue(question)

            depth -= 1

    def __get_questions_tags(self):
        paa_block = self.paa_block
        return paa_block.find_elements(By.XPATH, "//div[contains(@class, 'related-question-pair')]//div[@role=\"button\" and not(@aria-label=\"Result options\")]")

    def get_questions(self):
        return [q.text for q in self.__get_questions_tags()]

    class Question:
        def __init__(self, question) -> None:
            self._question = question
            self._get_n_times = 5

        @property
        def question(self):
            if not self._get_n_times:
                raise ElementIsNotPaaQuestionError()

            self._get_n_times -=1
            return self._question
