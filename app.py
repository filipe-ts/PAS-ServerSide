from flask import Flask, jsonify
import requests
import pathlib
import os
from dotenv import load_dotenv
from urllib.parse import quote

basedir = pathlib.Path(__file__).parent.resolve()
load_dotenv(os.path.join(basedir, '.env'))

key = os.getenv("OMDB_KEY")
TMDB_TOKEN = os.getenv("TMDB_TOKEN")

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

@app.route("/movies/top-rated")
def get_top_rated_movies():
    url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_TOKEN}"
    }
    
    response = requests.get(url, headers=headers).json()
    
    if 'results' in response:
        movies = response['results']
        movie_list = [{"title": movie['title'], "overview": movie['overview'], "release_date": movie['release_date']} for movie in movies]
        return jsonify(movie_list)
    else:
        return "<p>Erro ao obter filmes.</p>"

if __name__ == "__main__":
    app.run(debug=True)
