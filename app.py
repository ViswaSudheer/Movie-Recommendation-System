import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path'],data['release_date'],data['vote_average']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarities[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters = []
    recommended_movies_url=[]
    movie_overview=[]
    movie_casts=[]
    director=[]
    release_date=[]
    movie_vote_average=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        #print(movie_id)
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch posters
        poster,date,rating=fetch_poster(movie_id)
        release_date.append(date)
        movie_vote_average.append(rating)
        recommended_movies_posters.append(poster)
        recommended_movies_url.append("https://www.themoviedb.org/movie/{}".format(movie_id))
        movie_overview.append(initial['overview'][initial['id']==movie_id].values[0])
        movie_casts.append(cast['cast'][cast['movie_id']==movie_id].values[0])
        director.append(cast['crew'][cast['movie_id']==movie_id].values[0])
    return recommended_movies, recommended_movies_posters, recommended_movies_url,movie_overview,movie_casts,director,release_date,movie_vote_average

movies_dict=pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

initial_dict=pickle.load(open('initial_file_dict.pkl', 'rb'))
initial = pd.DataFrame(initial_dict)

cast_dict=pickle.load(open('for_cast_file_dict.pkl', 'rb'))
cast = pd.DataFrame(cast_dict)

similarities = pickle.load(open('similarities.pkl', 'rb'))

st.title('Movies Recommender System')

selected_movie_name = st.selectbox(
    "Select movie name",
    movies['title'].values
)

if st.button("Recommend"):
    names,posters,url,overview,movie_cast,director,release_date,rating = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
        st.link_button("website", url[0] ,icon="🌎")


    with col2:
        st.text(names[1])
        st.image(posters[1])
        st.link_button("website", url[1],icon="🌎")

    with col3:
        st.text(names[2])
        st.image(posters[2])
        st.link_button("website", url[2],icon="🌎")

    with col4:
        st.text(names[3])
        st.image(posters[3])
        st.link_button("website", url[3],icon="🌎")

    with col5:
        st.text(names[4])
        st.image(posters[4])
        st.link_button("website", url[4],icon="🌎")
    st.text("")
    st.header("Overviews of the recommended movies",divider=True)
    for i in range(5):
        st.header("{}. ".format(i+1)+names[i])
        col1, col2 = st.columns(2)
        with col1:
            st.image(posters[i],width=300)

        with col2:
            st.subheader("Overview:")
            #overview=initial[initial['title'] == names[i]]['overview']
            st.write(overview[i])
            with st.expander("Movie Details"):
                st.write("Ratings: "+str(rating[i]))
                st.write("Release Date: "+release_date[i])
                st.write("Cast: ")
                st.write(", ".join(movie_cast[i]))
                st.write("Director: " + " ".join(director[i]))
            st.link_button("The movie's website link", url[0], icon="🌎")
