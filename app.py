import streamlit as st
from library_utils import load_library, save_library

# Load library from the file
if "library" not in st.session_state:
    st.session_state.library = load_library()

st.title("📚 Personal Library Manager")

# Function to add a book
def add_book():
    new_book = {
        "title": st.session_state.title,
        "author": st.session_state.author,
        "year": st.session_state.year,
        "genre": st.session_state.genre,
        "read": st.session_state.read
    }
    st.session_state.library.append(new_book)
    save_library(st.session_state.library)
    st.success(f"✅ '{new_book['title']}' added successfully!")

# Function to remove a book
def remove_book(book_title):
    st.session_state.library = [book for book in st.session_state.library if book["title"].lower() != book_title.lower()]
    save_library(st.session_state.library)
    st.success(f"🗑 '{book_title}' removed successfully!")

# Sidebar menu
menu = st.sidebar.radio("Menu", ["Add Book", "Remove Book", "Search Books", "View All Books", "Library Stats"])

# Add a book
if menu == "Add Book":
    with st.form("add_book_form"):
        st.text_input("Book Title", key="title")
        st.text_input("Author", key="author")
        st.number_input("Publication Year", min_value=0, step=1, key="year")
        st.text_input("Genre", key="genre")
        st.checkbox("Read?", key="read")
        submit = st.form_submit_button("Add Book")

        if submit:
            add_book()

# Remove a book
elif menu == "Remove Book":
    book_to_remove = st.selectbox("Select a book to remove", [b["title"] for b in st.session_state.library])
    if st.button("Remove Book"):
        remove_book(book_to_remove)

# Search for books
elif menu == "Search Books":
    search_term = st.text_input("Search by Title or Author").lower()
    results = [b for b in st.session_state.library if search_term in b["title"].lower() or search_term in b["author"].lower()]
    if results:
        st.write("🔍 Search Results:")
        for book in results:
            st.write(f"📖 {book['title']} by {book['author']} ({book['year']}) [{book['genre']}] - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.write("⚠ No matching books found.")

# Display all books
elif menu == "View All Books":
    if st.session_state.library:
        for book in st.session_state.library:
            st.write(f"📖 {book['title']} by {book['author']} ({book['year']}) [{book['genre']}] - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.write("📚 Your library is empty.")

# Display library statistics
elif menu == "Library Stats":
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read"])
    if total_books > 0:
        percentage_read = (read_books / total_books) * 100
        st.write(f"📊 *Total Books:* {total_books}")
        st.write(f"✅ *Books Read:* {read_books} ({percentage_read:.2f}%)")
    else:
        st.write("📊 No books in your library.")