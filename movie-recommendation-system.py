import pickle
import streamlit as st
import requests
import numpy as np

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')  # Use data.get() to handle None
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        # If poster_path is None, provide a default image or handle missing posters
        full_path = "https://example.com/default_movie_poster.jpg"
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:21]:  # Change this to recommend 20 movies
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Display a chat input widget.
st.chat_input("Say something")
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Display 4 rows of 5 movies each
    for i in range(20):  # Display up to 20 movies
        col = st.columns(2)
        col1 = col[0]
        col2 = col[1]

        col1.write(f"**{recommended_movie_names[i]}**")
        
        # Use Markdown and HTML to display the image with a unique identifier
        col1.markdown(f'<img src="{recommended_movie_posters[i]}" alt="poster-{i}" width="100%">', unsafe_allow_html=True)
        
        col1.caption("Click on the poster for details.")

        # Handle poster click event
        if col1.button(f"Download", key=f"button-{i}"):
            # Clear the previous content
            col2.empty()

            # Replace with actual movie details
            movie_details = f"**Movie Details for {recommended_movie_names[i]}**\n\nThis is a sample movie description for the movie."

            # Display movie details
            col2.markdown(movie_details)







