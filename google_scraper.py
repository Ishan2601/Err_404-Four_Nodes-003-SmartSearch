from selenium import webdriver
from time import sleep

google_config = {
    'url':"https://www.google.co.in/",
    'search_box_name':"q",
    'search_terms_box_class':"erkvQe",
    'search_suggestions':"sbl1"
}

text = "Elon Musk"
question_words = ["How", "What", "Why", "When", "Where", "Which", "Is"]

fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()
browser = webdriver.Firefox('C:/WebDriver/bin', firefox_options=fireFoxOptions)
browser.get(google_config['url'])

web = {}

for question in question_words:
    ques_box = browser.find_element_by_name(google_config['search_box_name'])
    ques_box.send_keys(f"{question_words} {text}")
    sleep(1)
    search_term_box = browser.find_element_by_class_name(google_config['search_terms_box_class'])
    suggestions_elems = search_term_box.find_elements_by_class_name(google_config['search_suggestions'])
    suggestions = [i.text for i in suggestions_elems]

    web[question] = suggestions
    ques_box.clear()

print(web)


