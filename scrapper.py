from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from config import GoogleSearchConfig, YahooSearchConfig
from os import environ
from pytrends.request import TrendReq
import people_also_ask
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

#from webdriver_manager.chrome import ChromeDriverManager

class Scrapper:
    question_words = ["how", "what", "why", "when", "where", "which", "is"]

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
        cleaned_term = self._clean_term(search_term)

        google_search_ques = self.__get_google_search_ques(cleaned_term)
        yahoo_search_ques = self.__get_yahoo_search_ques(cleaned_term)
        
        questions = self.__result_combiner(google_search_ques, yahoo_search_ques)
        top_searches = self._get_top_searches(cleaned_term)
        prople_asks = self._people_also_ask(cleaned_term)

        return questions, top_searches, prople_asks

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
        pytrends = TrendReq()
        kw_list = [search_term]
        pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
        # pytrends.build_payload(kw_list)
        web = pytrends.related_topics()
        # web = pytrends.suggestions(kw_list)
        return web
    
    def _people_also_ask(self, search_term: str):
        web = people_also_ask.get_related_questions(search_term, 5)
        return web 

    def _clean_term(self, search_term: str):
        clean = []
        for word in word_tokenize(search_term):
            if word not in set(stopwords.words('english')):
                if word not in self.question_words:
                    clean.append(word)
        clean_s = ' '.join(clean)
        return clean_s
