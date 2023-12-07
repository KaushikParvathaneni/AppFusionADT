import streamlit as st
import pandas as pd
import sqlite3


st.title("ADT Final Project - Fall 2023")
st.title("AppFusion: Where Apps Align with Your Desire")
st.header("GROUP:")
st.header("Anushree Kolhe")
st.header("Shubhangi Dabral")
st.header("Kaushik Parvathaneni")
          

def read_data():
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query("SELECT * FROM applications;", conn)
    conn.close()
    return df

def top_developers():
    conn = sqlite3.connect('database.db')
    top_dev_df = pd.read_sql_query("SELECT * FROM TopDevelopers LIMIT 10;", conn)
    conn.close()

    st.subheader("Top Developers by Total Apps Developed")
    st.table(top_dev_df)

    # Function to display free applications
def free_applications():
    conn = sqlite3.connect('database.db')
    free_apps_df = pd.read_sql_query("SELECT * FROM FreeApplications LIMIT 15;", conn)
    conn.close()

    st.subheader("Free Applications")
    st.table(free_apps_df)

# Function to display top-rated apps by genre
def top_rated_apps_by_genre(genre):
    conn = sqlite3.connect('database.db')
    query = f"SELECT * FROM TopRatedAppsByGenre WHERE genre = '{genre}' LIMIT 10;"
    top_rated_df = pd.read_sql_query(query, conn)
    conn.close()

    st.subheader(f"Top Rated {genre} Apps")
    st.table(top_rated_df)
    

# Streamlit app
def main():
    

    # Read data from SQLite database
    app_data = read_data()

    # Display basic information about the dataset
    st.subheader("Sampled App Data")
    st.dataframe(app_data.head(10))  # Display only top 10 rows

    # Sidebar for user interactions
    st.sidebar.header("Explore Data")

    # Filter by Genre
    selected_genre = st.sidebar.selectbox("Select Genre", app_data['Genre'].unique())
    genre_filtered_df = app_data[app_data['Genre'] == selected_genre]

    # Filter by Average User Rating
    min_rating = st.sidebar.slider("Minimum Average User Rating", min_value=0, max_value=5, value=3)
    rating_filtered_df = genre_filtered_df[genre_filtered_df['Avg_user_rating'] >= min_rating]

    # Filter by Size
    min_size = st.sidebar.slider("Minimum Size (MB)", min_value=0.0, max_value=500.0, value=0.0)
    size_filtered_df = rating_filtered_df[rating_filtered_df['Size'] >= min_size]

    # Display the final filtered results
    st.subheader("Top 10 Apps based on Filters")
    st.table(size_filtered_df.head(10))

if __name__ == "__main__":
    main()