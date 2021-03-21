class GoogleSearchConfig:
    url = "https://www.google.co.in/"
    search_box_name = "q"
    search_terms_box_class = "erkvQe"
    search_suggestions = "sbl1"

class YahooSearchConfig:
    url = "https://in.search.yahoo.com/"
    search_box_name = "p"
    search_terms_box_class = "sa-tray-list-container"

class QuoraConfig:
    url = "https://www.quora.com/search?type=question&q="
    qbox_xpath = '//*[@id="root"]/div/div/div/div/div[4]/div/div/div[2]/div/div'
    ques_class = "CssComponent-sc-1oskqb9-0"