from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from cryptography.fernet import Fernet
import json
from flask_jwt_extended import create_access_token, JWTManager
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key
app.config['DEBUG'] = True
app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Set the login view (function name) for unauthorized users
jwt = JWTManager(app)

SECRET_KEY = b'some_secret_key'

# User model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(60), nullable=False)
    encryption_key = db.Column(db.String(255), nullable=False)
    credentials = db.Column(db.JSON)

# Flask-Login callback to reload the user object
@login_manager.user_loader
def load_user(email):
    return User.query.get(email)

# Endpoint for user authentication
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.hashed_password, password):
        # Use create_access_token to generate a JWT token
        token = create_access_token(identity=user.email)

        return jsonify({'token': token, 'message': 'Login successful'}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

# Endpoint for user logout
@app.route('/logout', methods=['POST'])
@login_required  # Requires a logged-in user to access the endpoint
def logout():
    logout_user()  # Log out the user
    return jsonify({'message': 'Logout successful'}), 200

# Endpoint for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check for valid email format
    if '@' not in email or '.' not in email.split('@')[-1]:
        return jsonify({'message': 'Invalid email format'}), 400

    # Check if the email is already registered
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 400

    # Check password criteria (you can customize this based on your requirements)
    if len(password) < 6:
        return jsonify({'message': 'Password must be at least 6 characters'}), 400

    # Hash the password before storing it in the database
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Generate a unique encryption key for the user
    encryption_key = generate_encryption_key()  # You should generate a secure key

    # Create a new user
    new_user = User(email=email, hashed_password=hashed_password, encryption_key=encryption_key)
    db.session.add(new_user)

    try:
        db.session.commit()

        # Log in the user after successful registration
        login_user(new_user)

        return jsonify({'message': 'User registered and logged in successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

def generate_encryption_key():
    return Fernet.generate_key().decode('utf-8')

def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
    # Convert the encrypted data to a string
    return encrypted_data.decode('utf-8')

def decrypt_data(encrypted_data, key):
    try:
        cipher_suite = Fernet(key)
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')
        return decrypted_data
    except Exception as e:
        print(f"Error decrypting data: {str(e)}")
        return '[]'  # Return an empty list as a string in case of an error

# Endpoint for adding credentials
@app.route('/add_credentials', methods=['POST'])
@login_required  # Requires a logged-in user to access the endpoint
def add_credentials():
    data = request.get_json()
    website_name = data.get('website_name')
    website_username = data.get('website_username')
    website_password = data.get('website_password')

    # Check if all required data is provided
    if not all([website_name, website_username, website_password]):
        return jsonify({'message': 'Missing required data'}), 400

    # Get the current user
    user = current_user

    # Decrypt existing credentials using the user's encryption key
    decrypted_credentials_str = user.credentials or '[]'
    decrypted_credentials = json.loads(decrypt_data(decrypted_credentials_str, user.encryption_key))

    # Handle the case where decrypted_credentials is None or an empty list
    if not decrypted_credentials:
        decrypted_credentials = []

    # Add new credentials
    new_credentials = {
        'website_name': website_name,
        'website_username': website_username,
        'website_password': encrypt_data(website_password, user.encryption_key)
    }

    decrypted_credentials.append(new_credentials)

    # Convert credentials to JSON format before updating the database
    updated_credentials = json.dumps(decrypted_credentials)

    # Encrypt the updated credentials before storing in the database
    user.credentials = encrypt_data(updated_credentials, user.encryption_key)
    db.session.commit()

    return jsonify({'message': 'Credentials added successfully'}), 200

# Endpoint for viewing decrypted credentials
@app.route('/user/<email>/credentials', methods=['GET'])
def view_credentials(email):
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Decrypt and return credentials
    decrypted_credentials = user.credentials
    decrypted_credentials = json.loads(decrypt_data(decrypted_credentials, user.encryption_key))

    # Decrypt the passwords separately
    for credential in decrypted_credentials:
        decrypted_password = decrypt_data(credential['website_password'], user.encryption_key)
        credential['website_password'] = decrypted_password.decode('utf-8') if isinstance(decrypted_password, bytes) else decrypted_password

    return jsonify({'credentials': decrypted_credentials}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)