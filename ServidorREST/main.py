from flask import Flask, request, jsonify, render_template
import requests
import pickle
import os

app = Flask(__name__)

DATA_FILE = 'data.pkl'

# Function to load data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'rb') as file:
            return pickle.load(file)
    return {'books': []}

# Function to save data to file
def save_data(data):
    with open(DATA_FILE, 'wb') as file:
        pickle.dump(data, file)

# Load data at the start
data = load_data()
books = data['books']

# Function to fetch book data from Open Library API
def fetch_book_data(isbn):
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get(f"ISBN:{isbn}", {})
    return {}

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/search', methods=['GET'])
def search_book(title):
    # Base URL for Open Library search API
    search_url = "https://openlibrary.org/search.json"

    title = request.json.get('title')

    # Parameters for the search query
    params = {
        'title': title
    }

    # Send GET request to Open Library API
    response = requests.get(search_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        # Print the search results
        for book in data['docs']:
            print(f"Title: {book.get('title')}")
            print(f"Author: {book.get('author_name', ['Unknown'])[0]}")
            print(f"First Published Year: {book.get('first_publish_year')}")
            print()
    else:
        print(f"Error: {response.status_code}")

# Create a new book
@app.route('/books', methods=['POST'])
def add_book():
    isbn = request.json.get('isbn')
    if not isbn:
        return jsonify({'error': 'ISBN is required'}), 400
    
    book_data = fetch_book_data(isbn)
    if not book_data:
        return jsonify({'error': 'Book not found'}), 404
    
    book = {
        'isbn': isbn,
        'title': book_data.get('title'),
        'authors': [author['name'] for author in book_data.get('authors', [])],
        'cover': book_data.get('cover', {}).get('large'),
        'reviews': []
    }
    books.append(book)
    save_data({'books': books})
    return jsonify(book), 201

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200

# Add a review to a book
@app.route('/books/<isbn>/reviews', methods=['POST'])
def add_review(isbn):
    book = next((b for b in books if b['isbn'] == isbn), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    review = {
        'reviewer': request.json.get('reviewer'),
        'text': request.json.get('text'),
        'rating': request.json.get('rating')
    }
    book['reviews'].append(review)
    save_data({'books': books})
    return jsonify(review), 201

# Get all reviews for a book
@app.route('/books/<isbn>/reviews', methods=['GET'])
def get_reviews(isbn):
    book = next((b for b in books if b['isbn'] == isbn), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book['reviews']), 200

if __name__ == '__main__':
    app.run(debug=True)