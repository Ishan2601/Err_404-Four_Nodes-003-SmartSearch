from app import app
from flask import request, render_template 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
from time import sleep
'''
def scrape_google(text):
	#text = "Elon Musk"

	fireFoxOptions = webdriver.FirefoxOptions()
	fireFoxOptions.set_headless()
	browser = webdriver.Firefox('C:/WebDriver/bin', firefox_options=fireFoxOptions)
	google_config = {
	    'url':"https://www.google.co.in/",
	    'search_box_name':"q",
	    'search_terms_box_class':"erkvQe",
	    'search_suggestions':"sbl1"
	}

	question_words = ["How", "What", "Why", "When", "Where", "Which", "Is"]

	browser.get(google_config['url'])

	all_questions = {}

	for question in question_words:
	    ques_box = browser.find_element_by_name(google_config['search_box_name'])
	    ques_box.send_keys(f"{question_words} {text}")
	    sleep(1)
	    search_term_box = browser.find_element_by_class_name(google_config['search_terms_box_class'])
	    suggestions_elems = search_term_box.find_elements_by_class_name(google_config['search_suggestions'])
	    suggestions = [i.text for i in suggestions_elems]

	    all_questions[question] = suggestions
	    ques_box.clear()
	return all_questions
'''
def scrape(text):
	chromeOptions = webdriver.ChromeOptions()
	chromeOptions.add_argument("--headless")
	chromeOptions.add_argument("--disable-dev-shm-usage")
	chromeOptions.add_argument("--no-sandbox")
	#chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
	browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chromeOptions)#webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

	question_words = ["How", "What", "Why", "When", "Where", "Which", "Is", "Does"]

	# Code for google scraper
	google_config = {
	    'url':"https://www.google.co.in/",
	    'search_box_name':"q",
	    'search_terms_box_class':"erkvQe",
	    'search_suggestions':"sbl1"
	}

	browser.get(google_config['url'])

	all_questions = {}

	for question in question_words:
	    ques_box = browser.find_element_by_name(google_config['search_box_name'])
	    ques_box.send_keys(f"{question_words} {text}")
	    sleep(1)
	    search_term_box = browser.find_element_by_class_name(google_config['search_terms_box_class'])
	    suggestions_elems = search_term_box.find_elements_by_class_name(google_config['search_suggestions'])
	    suggestions = [i.text for i in suggestions_elems]

	    all_questions[question] = suggestions
	    ques_box.clear()
	return all_questions



@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        search_term = request.form.get("searchquery")
        result = scrape(search_term)
        
    return render_template("index.html", result = result)