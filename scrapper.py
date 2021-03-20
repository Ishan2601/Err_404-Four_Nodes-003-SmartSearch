from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from config import GoogleSearchConfig, YahooSearchConfig
from os import environ
from pytrends.request import TrendReq

#from webdriver_manager.chrome import ChromeDriverManager

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
        
        #self.brow = webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=self.options)  

    def __result_combiner(self, *args):
        final_result = {i:[] for i in self.question_words}
        for result in args:
            for i in self.question_words:
                if i in result:
                    final_result[i].extend(result[i])
        return final_result

    def search_term(self, search_term : str):
        google_search_ques = self.__get_google_search_ques(search_term)
        yahoo_search_ques = self.__get_yahoo_search_ques(search_term)
        
        questions = self.__result_combiner(google_search_ques, yahoo_search_ques)
        top_searches = self._get_top_searches(search_term)

        return questions, top_searches

    def __get_google_search_ques(self, search_term : str):
        config = GoogleSearchConfig()
        self.brow.get(config.url)
        web = {}

        for prepend in self.question_words:
            ques_box = self.brow.find_element_by_name(config.search_box_name)
            ques_box.send_keys(f"{prepend} {search_term}")
            sleep(0.5)
            try:
                search_term_box = self.brow.find_element_by_class_name(config.search_terms_box_class)
                suggestions_elems = search_term_box.find_elements_by_class_name(config.search_suggestions)
                suggestions = [i.text for i in suggestions_elems]
                web[prepend] = suggestions
            except Exception:
                pass
            ques_box.clear()
        return web

    def __get_yahoo_search_ques(self, search_term : str):
        config = YahooSearchConfig()
        self.brow.get(config.url)
        web = {}

        for prepend in self.question_words:
            print(f"{prepend} {search_term}")
            ques_box = self.brow.find_element_by_name(config.search_box_name)
            ques_box.send_keys(f"{prepend} {search_term}")
            sleep(1)
            try:
                search_term_box = self.brow.find_element_by_class_name(config.search_terms_box_class)
                suggestions = search_term_box.text.split("\n")
                web[prepend] = suggestions
            except Exception:
                pass
            
            ques_box.clear()
        return web
    
    def _get_top_searches(self, search_term: str):
        pytrends = TrendReq(hl='en-US', tz=360)
        kw_list = [search_term]
        pytrends.build_payload(kw_list)
        web = pytrends.related_topics()
        # web = pytrends.suggestions(kw_list)
        return web

    




