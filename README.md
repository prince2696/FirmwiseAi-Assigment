# Bookstore Management System API

## Overview
This documentation outlines the RESTful API for the Bookstore Management System. The API allows 
users to add, retrieve, update, and delete book information. It's built using Python with the Flask 
framework and SQL Alchemy ORM, supporting basic and JWT authentication.
## Features

- **Database Schema**: Utilizes a MySQL database to store book details, including title, author, ISBN, price, and quantity.
- **API Endpoints**: Provides endpoints for performing CRUD operations on books:
  - Adding a new book
  - Retrieving all books
  - Retrieving a specific book by ISBN
  - Updating book details
  - Deleting a book
- **Authentication**: Implements basic authentication to restrict access to certain endpoints.
- **Documentation**: Includes Swagger for clear documentation of API endpoints and usage.
- **Testing**: Provides unit tests for the API endpoints to ensure functionality and handle edge cases and errors effectively.

## Technologies Used

- Flask: Python web framework for developing the RESTful API.
- Flask-SQLAlchemy: SQLAlchemy integration for database management.
- Flask-HTTPAuth: Library for implementing basic authentication in Flask applications.
- Flask-Swagger: Integration of Swagger/OpenAPI Specification for API documentation.
- MySQL: Relational database management system for storing book details.

#### Authentication
- **Login Endpoint:**
 - **URL:** `/auth/login`
 - **Method:** POST
 - **Body:** 
 - `username` - String
 - `password` - String
 - **Response:** JWT Token for authenticated requests.
#### Endpoints




Sample Data Creation
To create sample data, you can use the following example requests:
- **Add Books:**
 - **Endpoint:** `/books`
 - **Method:** POST
 - **Body:**
 ```json
 {
 "title": "The Great Gatsby",
 "author": "F. Scott Fitzgerald",
 "isbn": "1234567890",
 "price": 10.99,
 "quantity": 5
 }
 ```
 ```json
 {
 "title": "1984",
 "author": "George Orwell",
 "isbn": "1234567891",
 "price": 8.99,
 "quantity": 10
 }
 ```
#### Using the API
To use the API, follow these steps:
1. **Start the API Server:** Run the Flask application.
2. **Login:** Use the login endpoint to obtain a JWT token.
3. **Make Requests:** Use the provided endpoints to manage bookstore data.
10
Error Handling
All endpoints will return appropriate HTTP status codes for successful operations as well as for various errors 
(e.g., `400 Bad Request`, `401 Unauthorized`, `404 Not Found`, `500 Internal Server Error`)
