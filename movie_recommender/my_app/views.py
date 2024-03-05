
import json
from django.http import JsonResponse
from django.shortcuts import render
import pickle
import requests
import pandas as pd
import ast

movies=pd.read_csv('movies_data.csv')
similarity=pickle.load(open('similarity.pkl','rb'))


def loadIndex(request):
    return render(request, "base.html")


def getRecommendations(request):
    history = request.GET.get('history')
    print(history=='null')
    if history=='null':
        print("No history")
        movies, posters = get_randomMovie()
        print(movies)
        print(posters)
        movie_info = []
        movie_info.append({"movies": movies, "posters": posters})
        print("info" +str(movie_info))
        return JsonResponse({"recommended": movie_info})

    try:
        history_list = json.loads(history)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return JsonResponse({"error": "Invalid JSON"})

    recommendations = []
    for movie in history_list:
        if movie is not None:
            recommend_movies, movies_posters = recommend(movie)
            recommendations.append({"movies": recommend_movies, "posters": movies_posters})

    return JsonResponse({"recommended": recommendations})


    
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
def get_movie_index(movie_title):
    for index, title in enumerate(movies.keys()):
        if title == movie_title:
            return index
    return None 
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
 
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:
        
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        

    return recommended_movie_names,recommended_movie_posters
def get_randomMovie():
    suggested_movies=[]
    suggested_movies_posters = []
    for i,movie in movies.iterrows():
        if i<=7:
            movie_id=movie['movie_id']
            suggested_movies_posters.append(fetch_poster(movie_id))
            suggested_movies.append(movie['title'])
        else:
            break
    return suggested_movies,suggested_movies_posters
def get_search_movie(request):
    q = request.GET.get("q")
    q="zoesaldana"
    movie = movies[(movies['title'] == q) | (movies['tags'].str.contains(q))]
    search_data=[]
    print("title"+movie['title'])
    for i,m in movie.iterrows():
        movie_id=m['movie_id']
        poster=fetch_poster(movie_id)
        search_data.append({"title":m['title'],"poster":poster})
    return JsonResponse({"movies":search_data})


