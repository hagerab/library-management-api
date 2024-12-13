from flask import Flask, request, jsonify
from flasgger import Swagger
import json

app = Flask(__name__)
swagger = Swagger(app)

BOOKS_FILE = 'books.json'
try:
    with open(BOOKS_FILE, 'r') as file:
        books = json.load(file)
except FileNotFoundError:
    books = []

# Save data to JSON file
def save_books():
    with open(BOOKS_FILE, 'w') as file:
        json.dump(books, file)

@app.route('/books', methods=['POST'])
def add_book():
    """
    Add a new book
    ---
    tags:
      - Books
    parameters:
      - in: body
        name: book
        schema:
          type: object
          required:
            - title
            - author
            - published_year
            - isbn
          properties:
            title:
              type: string
            author:
              type: string
            published_year:
              type: integer
            isbn:
              type: string
            genre:
              type: string
    responses:
      200:
        description: Book added successfully
    """
    book = request.json
    books.append(book)
    save_books()
    return jsonify({"message": "Book added successfully", "book": book}), 200

@app.route('/books', methods=['GET'])
def list_books():
    """
    List all books
    ---
    tags:
      - Books
    responses:
      200:
        description: A list of books
    """
    return jsonify(books), 200

@app.route('/books/search', methods=['GET'])
def search_books():
    """
    Search for books
    ---
    tags:
      - Books
    parameters:
      - in: query
        name: author
        type: string
      - in: query
        name: year
        type: integer
      - in: query
        name: genre
        type: string
    responses:
      200:
        description: A list of books
    """
    author = request.args.get('author')
    year = request.args.get('year', type=int)
    genre = request.args.get('genre')

    results = [book for book in books if
               (not author or book.get('author') == author) and
               (not year or book.get('published_year') == year) and
               (not genre or book.get('genre') == genre)]
    return jsonify(results), 200

@app.route('/books/<isbn>', methods=['PUT'])
def update_book(isbn):
    """
    Update book details
    ---
    tags:
      - Books
    parameters:
      - in: path
        name: isbn
        type: string
        required: true
      - in: body
        name: book
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
            published_year:
              type: integer
            genre:
              type: string
    responses:
      200:
        description: Book updated successfully
      404:
        description: Book not found
    """
    updated_data = request.json
    for book in books:
        if book['isbn'] == isbn:
            book.update(updated_data)
            save_books()
            return jsonify({"message": "Book updated successfully", "book": book}), 200
    return jsonify({"error": "Book not found"}), 404

@app.route('/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    """
    Delete a book
    ---
    tags:
      - Books
    parameters:
      - in: path
        name: isbn
        type: string
        required: true
    responses:
      200:
        description: Book deleted successfully
      404:
        description: Book not found
    """
    global books
    book_exists = any(book['isbn'] == isbn for book in books)
    if not book_exists:
        return jsonify({"error": "Book not found"}), 404

    books = [book for book in books if book['isbn'] != isbn]
    save_books()
    return jsonify({"message": "Book deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
