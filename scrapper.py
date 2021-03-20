from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from config import GoogleSearchConfig
from os import environ

class Scrapper:
    question_words = ["How", "What", "Why", "When", "Where", "Which", "Is"]

    def __init__(self):
        self.options = Options()
        self.options.headless = True
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.binary_location = environ.get("GOOGLE_CHROME_BIN")
        self.brow = webdriver.Chrome(executable_path=environ.get("CHROMEDRIVER_PATH"),options=self.options) 

    def search_term(self, search_term : str):
        google_search_ques = self.__get_google_search_ques(search_term)

        return google_search_ques

    def __get_google_search_ques(self, search_term : str):
        config = GoogleSearchConfig()
        self.brow.get(config.url)
        web = {}

        for prepend in self.question_words:
            ques_box = self.brow.find_element_by_name(config.search_box_name)
            ques_box.send_keys(f"{prepend} {search_term}")
            sleep(1)
            search_term_box = self.brow.find_element_by_class_name(config.search_terms_box_class)
            suggestions_elems = search_term_box.find_elements_by_class_name(config.search_suggestions)
            suggestions = [i.text for i in suggestions_elems]

            web[prepend] = suggestions
            ques_box.clear()

        return web





