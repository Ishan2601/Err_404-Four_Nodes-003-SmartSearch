from os import environ
from time import sleep
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from config import GoogleSearchConfig, YahooSearchConfig, QuoraConfig

from pytrends.request import TrendReq
import people_also_ask
from utils import Utils

class Scrapper:
    question_words = ["how", "what", "why", "when", "where", "which", "is"]

    def __init__(self):
        options = self.__get_browser_options()
        self.brow = webdriver.Chrome(executable_path=environ.get("CHROMEDRIVER_PATH"),options=options)
        
    #    self.brow = webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=options)  
    
    def __get_browser_options(self) -> Options:
        """ Returns browser options"""
        options = Options()
        options.headless = True
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-dev-shm-usage")
        options.binary_location = environ.get("GOOGLE_CHROME_BIN")

        return options

    def __result_combiner(self, *args) -> Dict[str,List[str]]:
        final_result = {i:[] for i in self.question_words}
        for result in args:
            for i in self.question_words:
                if i in result:
                    final_result[i].extend(result[i])
        return final_result

    def process(self, search_term : str):
        """ Processes the search term """
        cleaned_term = Utils.clean_term(search_term)
        questions = self.__get_questions(cleaned_term)
        top_searches = self.__get_top_searches(search_term)
        people__ask = self.__people_also_ask(search_term)

        return questions, top_searches, people__ask
    
    def __get_questions(self, search_term : str) -> Dict[str,List[str]]:
        """ Acquires questions from multiple sources """
        google_search_ques = self.__get_google_search_ques(search_term)
        yahoo_search_ques = self.__get_yahoo_search_ques(search_term)
        quora_seach_ques = self.__get_quora_search_ques(search_term)

        questions = self.__result_combiner(google_search_ques, yahoo_search_ques, quora_seach_ques)
        return questions

    def __get_google_search_ques(self, search_term : str) -> Dict[str,List[str]]:
        """ Scrape popular questions from google search suggestions """
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

    def __get_yahoo_search_ques(self, search_term : str) -> Dict[str,List[str]]:
        """ Scrape popular questions from yahoo search suggestions """
        config = YahooSearchConfig()
        self.brow.get(config.url)
        web = {}

        for prepend in self.question_words:
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
        print("Yahoo")
        print(web)
        return web

    def __get_quora_search_ques(self, search_term : str) -> Dict[str,List[str]]:
        """ Scrape questions from quora questions page """
        config = QuoraConfig()
        search_term = search_term.replace("&", "%26")

        url = config.url + search_term
        self.brow.get(url)
        web = {i:[] for i in self.question_words}
        qbox = self.brow.find_element_by_xpath(config.qbox_xpath)
        questions_box = qbox.find_elements_by_class_name(config.ques_class)
        questions = [i.text for i in questions_box]
        questions = [i.split("\n")[0] for i in questions]

        for q in questions:
            ask = q.split()[0]
            if ask.lower() in web:
                web[ask.lower()].append(q)
        return web
    
    def __get_top_searches(self, search_term: str):
        
        pytrends = TrendReq()
        kw_list = [search_term]
        try:
            pytrends.build_payload(kw_list)
            web = pytrends.related_topics()
            # web = pytrends.suggestions(kw_list)
        except Exception:
            web = False
        return web
    
    def __people_also_ask(self, search_term: str):
        web = people_also_ask.get_related_questions(search_term, 5)
        return web 
