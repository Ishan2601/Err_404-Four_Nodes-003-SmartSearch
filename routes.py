from app import app
from flask import request, render_template 
from selenium import webdriver
import os
from time import sleep
from scrapper import Scrapper
from werkzeug.wrappers import Response
import csv
import json

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

@app.route("/getJson")
def getJson():
    with open("CSV/data.json") as f:
        json = f.read()
    response = Response(json, mimetype='text/json')
    response.headers.set("Content-Disposition", "attachment", filename="smart_search.json")
    return response
    

@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        search_term = request.form.get("searchquery")
        result, top_result, prople_asks, clusters, corpus, distances = scrp.process(search_term)
        with open('CSV/data.csv', 'w') as f:
            for key in result.keys():
                for v in result[key]:
                    #print((key,v))
                    try:
                        f.write("%s,%s\n"%(key,v))
                    except Exception:
                        continue
                    
        with open("CSV/data.json", "w") as outfile:  
            json.dump(result, outfile) 
        
    return render_template("index.html", result = result, top_result = top_result, prople_asks=prople_asks, searched = search_term, clusters= clusters, corpus=corpus, distances = distances)
