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
    st.title("AppFusion: Where Apps Align with Your Desire")

    # Read data from SQLite database
    app_data = read_data()

    # Display basic information about the dataset
    st.subheader("Sampled App Data")
    st.dataframe(app_data.head())

    # Sidebar for user interactions
    st.sidebar.header("Explore Data")

    # Filter by Genre
    selected_genre = st.sidebar.selectbox("Select Genre to View Top Rated Apps", app_data['Genre'].unique())
    top_rated_apps_by_genre(selected_genre)

    # Slider for Average User Rating
    min_rating = st.sidebar.slider("Minimum Average User Rating", min_value=0, max_value=5, value=3)
    filtered_apps = app_data[app_data['Avg_user_rating'] >= min_rating]

    # Display filtered apps
    st.subheader("Apps with Minimum Average User Rating")
    st.table(filtered_apps)

    # Display top developers
    top_developers()

    # Display free applications
    free_applications()

if __name__ == "__main__":
    main()