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

@app.route("/movies/search/<string:title>")
def search(title): 
    url = f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=false&language=pt-Br&page=1"
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_TOKEN}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            movies = data['results']
            movie_list = []
            for movie in movies:
                poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None
                backdrop_url = f"https://image.tmdb.org/t/p/w500{movie['backdrop_path']}" if movie.get('backdrop_path') else None
                
                movie_data = {
                    "title": movie['title'],
                    "overview": movie['overview'],
                    "release_date": movie['release_date'],
                    "vote_average": movie['vote_average'],
                    "vote_count": movie['vote_count'],
                    "poster_url": poster_url,
                    "backdrop_url": backdrop_url,
                }
                movie_list.append(movie_data)
            return jsonify(movie_list)
        else:
            return ""
    else:
        return ""

@app.route("/movies/top-rated")
def get_top_rated_movies():
    url = "https://api.themoviedb.org/3/movie/top_rated?language=pt-Br&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_TOKEN}"
    }
    
    response = requests.get(url, headers=headers).json()
    
    if 'results' in response:
        movies = response['results']
        movie_list = []
        for movie in movies:
            poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None
            
            backdrop_url = f"https://image.tmdb.org/t/p/w500{movie['backdrop_path']}" if movie.get('backdrop_path') else None
            
            movie_data = {
                "title": movie['title'],
                "overview": movie['overview'],
                "release_date": movie['release_date'],
                "poster_url": poster_url,
                "backdrop_url": backdrop_url
            }
            movie_list.append(movie_data)
        
        return jsonify(movie_list)
    else:
        return "<p>Erro ao obter filmes.</p>"

if __name__ == "__main__":
    app.run(debug=True)
