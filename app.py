# importing Flask
from flask import Flask

# Flask constructor 
app = Flask(__name__) 

from routes import *

if __name__=='__main__':  
    app.run(debug=True) 
