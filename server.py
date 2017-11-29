# flask server for handling the requests
from flask import Flask
import ts3_rest_api

app = Flask(__name__)

@app.route('/')
def index():
    return "hello"




