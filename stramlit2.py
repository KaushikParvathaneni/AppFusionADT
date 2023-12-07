from tarfile import PAX_NAME_FIELDS
import streamlit as st
import pandas as pd
import sqlite3
from PIL import Image, ImageEnhance
from io import BytesIO
import base64

st.markdown("<h1 style='text-align: center; font-size: 2.5em;''> AppFusion </h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: right;'> - Where Apps Align with Your Desire</h3>", unsafe_allow_html=True)  

def lighten_image(image_path, brightness_factor=1.0):
    img = Image.open(image_path)
    enhancer = ImageEnhance.Brightness(img)
    lightened_img = enhancer.enhance(brightness_factor)
    return lightened_img

def get_base64_from_image(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def set_background(image_path, brightness_factor= 1.0):
    lightened_img = lighten_image(image_path, brightness_factor)
    base64_img = get_base64_from_image(lightened_img)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
    }

    .body{
    color: #A45A52
    }
    </style>
    ''' % base64_img
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('blue.jpg', brightness_factor= 1.0)

# Function to create a new app
def create_app():
    st.subheader("Create a New App")

    # Get user input for a new app
    app_id = st.text_input("App_Id")
    app_name = st.text_input("App Name")
    developer_id = st.text_input("Developer ID")
    genre = st.text_input("Genre")
    size = st.text_input("Size (MB)")
    app_version = st.text_input("App Version")
    ios_version = st.text_input("iOS Version")
    released_date = st.text_input("Released Date (YYYY-MM-DD)")
    updated_date = st.text_input("Updated Date (YYYY-MM-DD)")
    avg_user_rating = st.text_input("Average User Rating")
    age_group = st.text_input("Age Group")

    # Validate and add the new app to the database
    if st.button("Create App"):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        insert_query = insert_query = """
            INSERT INTO applications (App_Id, App_name, Developer_Id, Genre, Size, App_version, IOS_version, Released_date, Updated_date, Avg_user_rating, Age_group)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        values = (
            app_id, app_name, developer_id, genre, size, app_version,
            ios_version, released_date, updated_date, avg_user_rating, age_group
        )

        c.execute(insert_query, values)
        conn.commit()
        conn.close()

        st.success("App created successfully!")

# Function to update an existing app
def update_app():
    st.subheader("Update an Existing App")

    # Get user input for updating an app
    app_id = st.text_input("App ID")
    # Fetch the existing app data based on the provided App ID and display it for editing
    existing_app_data = read_data()[read_data()['App_Id'] == app_id]
    
    if existing_app_data.empty:
        st.warning("App not found. Enter a valid App ID.")
        return

    st.table(existing_app_data)

    # Get updated values from the user
    updated_app_name = st.text_input("Updated App Name", existing_app_data.iloc[0]['App_Id'])
    updated_genre = st.text_input("Updated Genre", existing_app_data.iloc[0]['Genre'])
    # Add more fields to update as needed

    # Perform validation and update logic here (replace with your implementation)
    if st.button("Update App"):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        update_query = """
        UPDATE applications
        SET App_name=?, Genre=?
        WHERE App_id=?;
        """

        values = (
            updated_app_name, updated_genre, app_id
        )

        c.execute(update_query, values)
        conn.commit()
        conn.close()

        st.success("App updated successfully!")

# Function to read an existing app
def read_app():
    st.subheader("Read an Existing App")

    # Get user input for reading an app
    app_name_to_read = st.text_input("App name to read")

    # Fetch the existing app data based on the provided App name and display it for confirmation
    existing_app_data = read_data()[read_data()['App_name'] == app_name_to_read]

    if existing_app_data.empty:
        st.warning("App not found. Enter a valid App ID.")
        return
    
    st.table(existing_app_data)

    # Confirm reading
    if st.button("Read App"):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        read_query = """
        DELETE FROM applications
        WHERE App_name=?;
        """

        c.execute(read_query, (app_name_to_read,))
        conn.commit()
        conn.close()

        st.success("App read successfully!")

# Function to delete an existing app
def delete_app(): 
    st.subheader("Delete an Existing App")

    # Get user input for deleting an app
    app_id_to_delete = st.text_input("App ID to Delete")

    # Fetch the existing app data based on the provided App ID and display it for confirmation
    existing_app_data = read_data()[read_data()['App_Id'] == app_id_to_delete]

    if existing_app_data.empty:
        st.warning("App not found. Enter a valid App ID.")
        return

    st.table(existing_app_data)

    # Confirm deletion
    if st.button("Delete App"):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        delete_query = """
        DELETE FROM applications
        WHERE App_Id=?;
        """

        c.execute(delete_query, (app_id_to_delete,))
        conn.commit()
        conn.close()

        st.success("App deleted successfully!")

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

    search_term = st.sidebar.text_input("Search by App Name")
    if search_term:
        search_result_df = size_filtered_df[size_filtered_df['App_name'].str.contains(search_term, case=False)]
        st.subheader('Search results')
        st.table(search_result_df.head(10))


    st.title("Additional Information")

    # Additional Information Section
    st.sidebar.header("Additional Information")

   # Display top developers
    st.sidebar.subheader("Top Developers")
    top_developers()

    # Display free applications
    st.sidebar.subheader("Free Applications")
    free_applications()


    st.header('CRUD Operations')
    selected_action = st.selectbox("Select an action", ["Create App", "Update App", "Read App", "Delete App"])

# Call the corresponding function based on the selected action
    if selected_action == "Create App":
        create_app()
    elif selected_action == "Update App":
        update_app()
    elif selected_action == "Read App":
        read_app()
    elif selected_action == "Delete App":
        delete_app()

if __name__ == "__main__":
    main()

