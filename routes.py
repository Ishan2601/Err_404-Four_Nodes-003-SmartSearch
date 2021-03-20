from app import app
from flask import request, render_template 
from selenium import webdriver
import os
from time import sleep
from scrapper import Scrapper

scrp = Scrapper()

@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        search_term = request.form.get("searchquery")
        result = scrp.search_term(search_term)
        
    return render_template("index.html", result = result)