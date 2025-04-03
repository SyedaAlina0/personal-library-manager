import streamlit as st
import pandas as pd
import os

# File to store books
data_file = "library.csv"

# Load existing data if available
def load_data():
    if os.path.exists(data_file):
        return pd.read_csv(data_file)
    return pd.DataFrame(columns=["Title", "Author", "Genre", "Status"])

# Save data to CSV
def save_data(df):
    df.to_csv(data_file, index=False)

# Initialize data
library_df = load_data()

# Streamlit UI
st.title("📚 Personal Library Manager")

# Add a new book
st.sidebar.header("Add a New Book")
title = st.sidebar.text_input("Book Title")
author = st.sidebar.text_input("Author")
genre = st.sidebar.selectbox("Genre", ["Fiction", "Non-Fiction", "Mystery", "Sci-Fi", "Fantasy", "Other"])
status = st.sidebar.selectbox("Status", ["Not Read", "Reading", "Completed"])

if st.sidebar.button("Add Book"):
    if title and author:
        new_entry = pd.DataFrame([[title, author, genre, status]], columns=["Title", "Author", "Genre", "Status"])
        library_df = pd.concat([library_df, new_entry], ignore_index=True)
        save_data(library_df)
        st.sidebar.success("Book added successfully!")
    else:
        st.sidebar.error("Please enter both Title and Author.")

# Display book collection
st.subheader("📖 My Book Collection")

# Filter options
genre_filter = st.selectbox("Filter by Genre", ["All"] + list(library_df["Genre"].unique()))
status_filter = st.selectbox("Filter by Status", ["All", "Not Read", "Reading", "Completed"])

# Apply filters
filtered_df = library_df.copy()
if genre_filter != "All":
    filtered_df = filtered_df[filtered_df["Genre"] == genre_filter]
if status_filter != "All":
    filtered_df = filtered_df[filtered_df["Status"] == status_filter]

st.dataframe(filtered_df)

# Allow deleting books
st.sidebar.header("Remove a Book")
book_to_remove = st.sidebar.selectbox("Select a Book", ["None"] + list(library_df["Title"]))
if st.sidebar.button("Remove Book") and book_to_remove != "None":
    library_df = library_df[library_df["Title"] != book_to_remove]
    save_data(library_df)
    st.sidebar.success("Book removed successfully!")

st.sidebar.info("Reload the page after adding or removing books to see updates.")