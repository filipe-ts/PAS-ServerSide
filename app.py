from flask import Flask, json, jsonify
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

@app.route("/movies/search/<int:movie_id>")
def search(movie_id): 
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=pt-BR"
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_TOKEN}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        data = response.json()
        
        poster_url = f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data.get('poster_path') else None
        backdrop_url = f"https://image.tmdb.org/t/p/w500{data['backdrop_path']}" if data.get('backdrop_path') else None
        
        movie_data = {
            "title": data.get('title', 'Título não disponível'),
            "overview": data.get('overview', 'Descrição não disponível'),
            "release_date": data.get('release_date', 'Data não disponível'),
            "vote_average": data.get('vote_average', 0),
            "vote_count": data.get('vote_count', 0),
            "poster_url": poster_url,
            "backdrop_url": backdrop_url,
        }
        
        return jsonify(movie_data)
    
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": f"HTTP error: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        return jsonify({"error": f"Request error: {req_err}"}), 500
    except KeyError:
        return jsonify({"error": "Unexpected response format from API"}), 500

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
                "id": movie['id'],
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
