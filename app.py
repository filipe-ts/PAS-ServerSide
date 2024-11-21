from flask import Flask
import requests
import pathlib
import os
from dotenv import load_dotenv
import json

basedir = pathlib.Path(__file__).parent.resolve()
load_dotenv(os.path.join(basedir, '.env'))

key = os.getenv("OMDB_KEY")

app = Flask(__name__)

@app.route("/<string:title>")
def get_title(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={key}"
    response = json.loads(requests.get(url=url).text)
    return f"<p>{response["Title"]}</p>"

@app.route("/search/<string:title>")
def search(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={key}"
    response = requests.get(url=url)
    return f"<p>{response.text}</p>"