import unittest
import json
from app import app, db, User, Book

class BookstoreAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_bookstore.db'
        app.config['TESTING'] = True

        with app.app_context():
            db.create_all()
            user = User(username="testuser", password="testpassword")
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_user_registration(self):
        response = self.app.post('/register', data=json.dumps({'username': 'newuser', 'password': 'newpassword'}), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', data['message'])

    def test_user_login(self):
        response = self.app.post('/login', data=json.dumps({'username': 'testuser', 'password': 'testpassword'}), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in data)

    def test_add_book(self):
        login_response = self.app.post('/login', data=json.dumps({'username': 'testuser', 'password': 'testpassword'}), content_type='application/json')
        token = json.loads(login_response.data)['token']
        book_data = {'title': 'Test Book', 'author': 'Test Author', 'isbn': '1234567890123', 'price': 10.99, 'quantity': 5}
        response = self.app.post('/book', headers={'Authorization': f'Bearer {token}'}, data=json.dumps(book_data), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('New book added', data['message'])

if __name__ == "__main__":
    unittest.main()
