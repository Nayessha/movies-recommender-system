import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests
import time
import os

API_KEY = os.getenv("TMDB_API_KEY")




def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={"0729d5caed5e134c2ef32246d36d4dc8"}"


    try:
        response = requests.get(
            url

        )

        data = response.json()


        if 'poster_path' in data and data['poster_path']:

            return "https://image.tmdb.org/t/p/w500" + data['poster_path']
        elif 'logo_path' in data and data['logo_path']:

            return "https://image.tmdb.org/t/p/w500" + data['logo_path']
        elif 'backdrop_path' in data and data['backdrop_path']:

            return "https://image.tmdb.org/t/p/w500" + data['backdrop_path']

        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"

    except Exception as e:
        print(e)
        return fetch_poster(movie_id)
        # return "https://th.bing.com/th?q=Creepy+Ventriloquist+Dummy&w=120&h=120&c=1&rs=1&qlt=70&o=7&cb=1&dpr=1.5&pid=InlineBlock&rm=3&mkt=en-IN&cc=IN&setlang=en&adlt=moderate&t=1&mw=247"
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    l_sort = sorted(list(enumerate(distances)),
                    reverse=True,
                    key=lambda x: x[1])[1:6]

    recommended_movies = []
    movie_poster=[]


    for i in l_sort:
        recommended_movies.append(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]].movie_id
        print(movie_id)
        movie_poster.append(fetch_poster(movie_id))
        # time.sleep(5)
    # print("movie_poster",movie_poster)

    return recommended_movies, movie_poster


st.title('Movie Recommender System')

selected_movie = st.selectbox(
    'Enter a movie',
    movies['title'].values
)

if st.button('Recommend'):
   names,posters = recommend(selected_movie)

   col1, col2, col3,col4,col5 = st.columns(5)
   with col1:
       st.text(names[0])
       st.image(posters[0])

   with col2:
       st.text(names[1])
       st.image(posters[1])

   with col3:
       st.text(names[2])
       st.image(posters[2])

   with col4:
       st.text(names[3])
       st.image(posters[3])

   with col5:
       st.text(names[4])
       st.image(posters[4])

