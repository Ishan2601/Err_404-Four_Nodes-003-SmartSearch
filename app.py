# importing Flask and other modules 
from flask import Flask, request, render_template 

# Flask constructor 
app = Flask(__name__) 

from routes import *

if __name__=='__main__':  
    app.run(debug=True) 
