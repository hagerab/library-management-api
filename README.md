# Library Management API

A Flask-based RESTful API for managing a collection of books in a library.
Dockerized for easy deployment.

## Features
- Add new books
- List all books
- Search books by author, year, or genre
- Update book details
- Delete books 
- Swagger documentation at `/apidocs`

## Setup Instructions
### 1. Clone the Repository
```
git clone https://github.com/yourusername/library-management-api.git
cd library-management-api
```
### 2. Set Up Python Environment
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the API
```

python app.py
```
Access the API at http://127.0.0.1:5000.

## Docker Instructions
### Build and Run
```
docker build -t library-api .
docker run -p 5000:5000 library-api
```
You can acces the API at http://localhost:5000


## Endpoints
| HTTP Method | Endpoint           | Description               |
|-------------|--------------------|---------------------------|
| POST        | `/books`           | Add a new book            |
| GET         | `/books`           | List all books            |
| GET         | `/books/search`    | Search for books          |
| PUT         | `/books/{isbn}`    | Update book details       |
| DELETE      | `/books/{isbn}`    | Delete a book by ISBN     |

