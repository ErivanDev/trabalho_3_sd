from flask import Flask, request, jsonify, render_template, Response
import requests
import pickle
import os

from dicttoxml import dicttoxml
import library_pb2

app = Flask(__name__)

DATA_FILE = 'data.pkl'

# Convert to protobuf
def convert_to_protobuf(data):
    books_proto = library_pb2.Books()
    for book in data:
        book_proto = books_proto.books.add()
        book_proto.id = book['id']
        book_proto.isbn = book['isbn']
        book_proto.title = book['title']
        book_proto.authors.extend(book['authors'])
        book_proto.cover = book['cover']
        for review in book['reviews']:
            review_proto = book_proto.reviews.add()
            review_proto.id = review['id']
            review_proto.reviewer = review['reviewer']
            review_proto.text = review['text']
            review_proto.rating = float(review['rating'])
    return books_proto.SerializeToString()

# Utility function to convert data to XML or JSON
def convert_response(data, response_format):
    if response_format == 'json':
        return jsonify(data)
    elif response_format == 'xml':
        xml_data = dicttoxml(data, custom_root='response', attr_type=False)
        return Response(xml_data, mimetype='application/xml')
    elif response_format == 'protobuf':
        return Response(convert_to_protobuf(data), mimetype='application/x-protobuf')

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
def search_book():
    # Base URL for Open Library search API
    search_url = "https://openlibrary.org/search.json"

    title = request.args.get('title')
    limit = request.args.get('limit')

    # Parameters for the search query
    params = {
        'title': title,
        'limit': limit
    }

    # Send GET request to Open Library API
    response = requests.get(search_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        return data, 200
    else:
        return jsonify({'error': 'Books not found'}), 404

# Create a new book
'''
@app.route('/books', methods=['POST'])
def add_book():
    isbn = request.json.get('isbn')
    if not isbn:
        return jsonify({'error': 'ISBN is required'}), 400
    
    book_data = fetch_book_data(isbn)
    if not book_data:
        return jsonify({'error': 'Book not found'}), 404
    
    book_id_counter = 1 if len(data['books']) == 0 else data['books'][len(data['books'])-1]['id'] + 1
    
    book = {
        'id': book_id_counter,
        'isbn': isbn,
        'title': book_data.get('title'),
        'authors': [author['name'] for author in book_data.get('authors', [])],
        'cover': book_data.get('cover', {}).get('large'),
        'reviews': []
    }
    books.append(book)
    save_data({'books': books})
    return jsonify(book), 201
'''

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    response_format = request.args.get('format', 'json')

    return convert_response(books, response_format)

    # return jsonify(books), 200

# Add a review to a book
@app.route('/books/<isbn>/reviews', methods=['POST'])
def add_review(isbn):
    book = next((b for b in books if b['isbn'] == isbn), None)
    if not book:
        # return jsonify({'error': 'Book not found'}), 404
        book_data = fetch_book_data(isbn)
        if not book_data:
            return jsonify({'error': 'Book not found'}), 404
        
        book_id_counter = 1 if len(data['books']) == 0 else data['books'][len(data['books'])-1]['id'] + 1
    
        book = {
            'id': book_id_counter,
            'isbn': isbn,
            'title': book_data.get('title'),
            'authors': [author['name'] for author in book_data.get('authors', [])],
            'cover': book_data.get('cover', {}).get('large'),
            'reviews': []
        }
        books.append(book)
        save_data({'books': books})
    
    review_id_counter = 1 if len(book['reviews']) == 0 else book['reviews'][len(book['reviews'])-1]['id'] + 1

    review = {
        'id': review_id_counter,
        'reviewer': request.json.get('reviewer'),
        'text': request.json.get('text'),
        'rating': request.json.get('rating')
    }
    book['reviews'].append(review)
    save_data({'books': books})
    return jsonify(review), 201

# Update a review to a book
@app.route('/books/<isbn>/reviews/<int:id>', methods=['PUT'])
def update_review(isbn, id):
    book = next((b for b in books if b['isbn'] == isbn), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    review = next((r for r in book['reviews'] if r['id'] == id), None)
    if not review:
        return jsonify({'error': 'Review not found'}), 404

    review_data = request.json
    if 'reviewer' in review_data:
        review['reviewer'] = review_data['reviewer']
    if 'text' in review_data:
        review['text'] = review_data['text']
    if 'rating' in review_data:
        review['rating'] = review_data['rating']
    
    save_data({'books': books})
    return jsonify(review), 200

# Delete a review to a book
@app.route('/books/<isbn>/reviews/<int:id>', methods=['DELETE'])
def delete_review(isbn, id):
    book = next((b for b in books if b['isbn'] == isbn), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    reviews = [r for r in book['reviews'] if r['id'] != id]
    if len(reviews) == len(book['reviews']):
        return jsonify({'error': 'Review not found'}), 404

    for b in books:
        if b['isbn'] == isbn:
            b['reviews'] = reviews
            break
    
    save_data({'books': books})
    return jsonify(reviews), 200

# Get all reviews for a book
@app.route('/books/<isbn>/reviews', methods=['GET'])
def get_reviews(isbn):
    book = next((b for b in books if b['isbn'] == isbn), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book['reviews']), 200

if __name__ == '__main__':
    app.run(debug=True)