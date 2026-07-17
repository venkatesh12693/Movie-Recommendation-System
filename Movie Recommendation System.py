import streamlit as st
import requests

# 0. PAGE CONFIG
st.set_page_config(page_title="Movie Explorer", page_icon="🎬", layout="wide")

# 1. API CONFIGURATION
API_KEY = 'Movie Api Key' 
BASE_URL = "https://api.themoviedb.org/3"

st.title("🎬 Movie Explorer")

# 2. FETCH GENRES
@st.cache_data
def get_genres():
    url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}"
    response = requests.get(url).json()
    return {g['name']: g['id'] for g in response.get('genres', [])}

genre_map = get_genres()
selected_genres = st.multiselect("Select Genres:", options=list(genre_map.keys()))

# 3. FETCH CREDITS (Director, Producer, Cast)
def get_movie_details(movie_id):
    # Fetch Credits
    cred_url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}"
    cred_data = requests.get(cred_url).json()
    
    crew = cred_data.get('crew', [])
    # TMDB often lists multiple producers; we take the first one
    director = next((m['name'] for m in crew if m['job'] == 'Director'), 'N/A')
    producer = next((m['name'] for m in crew if m['job'] == 'Producer'), 'N/A')
    cast = [m['name'] for m in cred_data.get('cast', [])[:3]]
    
    return director, producer, cast

# 4. FETCH AND DISPLAY MOVIES
if selected_genres:
    genre_ids = [str(genre_map[g]) for g in selected_genres]
    url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_genres={','.join(genre_ids)}&sort_by=popularity.desc"
    
    movies = requests.get(url).json().get('results', [])

    st.subheader("Your Recommendations:")
    for movie in movies[:20]:
        # Fetch detailed info
        director, producer, cast = get_movie_details(movie['id'])
        
        # Display each movie in a custom card
        with st.container():
            col1, col2 = st.columns([1, 3])
            
            with col1:
                poster = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}"
                if movie.get('poster_path'):
                    st.image(poster, use_column_width=True)
                else:
                    st.info("No Poster")
            
            with col2:
                st.markdown(f"### {movie.get('title')}")
                st.markdown(f"**Description:** {movie.get('overview')}")
                st.markdown(f"**Director:** {director} | **Producer:** {producer}")
                st.markdown(f"**Cast:** {', '.join(cast)}")
            
            st.markdown("---")
else:
    st.info("👈 Select genres to begin exploring.")