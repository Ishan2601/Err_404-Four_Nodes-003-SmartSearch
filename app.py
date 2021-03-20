# importing Flask and other modules 
from flask import Flask, request, render_template 
import numpy as np
import pandas as pd

# Flask constructor 
app = Flask(__name__) 

@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        result = request.form.get("searchquery")
        
    return render_template("index.html", result = result)
	
 
if __name__=='__main__':  
    app.run(debug=True) 
