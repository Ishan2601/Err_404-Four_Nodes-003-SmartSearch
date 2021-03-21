from app import app
from flask import request, render_template 
from selenium import webdriver
import os
from time import sleep
from scrapper import Scrapper
from werkzeug.wrappers import Response
import csv

scrp = Scrapper()

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/getPlotCSV")
def getPlotCSV():
    with open("CSV/data.csv") as f:
        csv = f.read()
    response = Response(csv, mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename="smart_search.csv")
    return response
    

@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        search_term = request.form.get("searchquery")
        result, top_result, prople_asks = scrp.process(search_term)
        with open('CSV/data.csv', 'w') as f:
            for key in result.keys():
                for v in result[key]:
                    f.write("%s,%s\n"%(key,v))
        
    return render_template("index.html", result = result, top_result = top_result, prople_asks=prople_asks, searched = search_term)
