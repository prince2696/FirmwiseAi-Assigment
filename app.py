from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime

# Initialize app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Database model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    isbn = db.Column(db.String(13), unique=True)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

# User model for authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

# Create the database
with app.app_context():
    db.create_all()

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password']) 
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        token = create_access_token(identity=data['username'])
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Endpoint for adding a new book
@app.route('/book', methods=['POST'])
@jwt_required()
def add_book():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], isbn=data['isbn'], price=data['price'], quantity=data['quantity'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'New book added!'}), 201

# Endpoint for getting all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data = {'title': book.title, 'author': book.author, 'isbn': book.isbn, 'price': book.price, 'quantity': book.quantity}
        output.append(book_data)
    return jsonify({'books': output})

# Endpoint for getting a single book
@app.route('/book/<isbn>', methods=['GET'])
def get_one_book(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    if not book:
        return jsonify({'message': 'No book found!'})
    book_data = {'title': book.title, 'author': book.author, 'isbn': book.isbn, 'price': book.price, 'quantity': book.quantity}
    return jsonify(book_data)

# Endpoint for deleting a book
@app.route('/book/<isbn>', methods=['DELETE'])
@jwt_required()
def delete_book(isbn):
    current_user = get_jwt_identity()
    book = Book.query.filter_by(isbn=isbn).first()
    if not book:
        return jsonify({'message': 'No book found!'})
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'The book has been deleted!'})


# Endpoint for updating a book
@app.route('/book/<isbn>', methods=['PUT'])
@jwt_required()
def update_book(isbn):
    current_user = get_jwt_identity()
    book = Book.query.filter_by(isbn=isbn).first()

    if not book:
        return jsonify({'message': 'No book found!'})

    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.price = data.get('price', book.price)
    book.quantity = data.get('quantity', book.quantity)

    db.session.commit()
    return jsonify({'message': 'Book updated successfully!'})



if __name__ == '__main__':
    app.run(debug=True)

