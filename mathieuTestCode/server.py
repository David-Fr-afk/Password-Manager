from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from cryptography.fernet import Fernet
from sqlalchemy.exc import IntegrityError
import json
from flask_bcrypt import check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, token_in_blocklist_loader

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'your_secret_key'

# Configuration for Flask JWT Extended
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

# In-memory set to store blacklisted tokens
blacklisted_tokens = set()

# User model
class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(120), primary_key=True, unique=True, nullable=False)
    hashed_password = db.Column(db.String(60), nullable=False)
    encryption_key = db.Column(db.String(255), nullable=False)
    credentials = db.Column(db.JSON)


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklisted_tokens

# Set the token in the blacklist when it expires
@jwt.expired_token_loader
def expired_token_callback(expired_token):
    jti = expired_token['jti']
    blacklisted_tokens.add(jti)
    return jsonify({'message': 'Token has expired'}), 401

# Endpoint for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check for valid email format
    if not is_valid_email(data['email']):
        return jsonify({'message': 'Invalid email format'}), 400

    # Check if the email is already registered
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400

    # Hash the password before storing it in the database
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Generate a unique encryption key for the user
    encryption_key = Fernet.generate_key().decode('utf-8')

    # Create a new user
    new_user = User(email=data['email'], hashed_password=hashed_password, encryption_key=encryption_key)
    db.session.add(new_user)

    try:
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Email already registered'}), 400

# Endpoint for user deletion
@app.route('/user/<email>', methods=['DELETE'])
def delete_user(email):
    user = User.query.get(email)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'message': 'User not found'}), 404

# Endpoint for user retrieval
@app.route('/user/<email>', methods=['GET'])
def get_user(email):
    user = User.query.get(email)
    if user:
        user_data = {
            'email': user.email,
            'encryption_key': user.encryption_key,
            'credentials': decrypt_credentials(user.credentials, user.encryption_key)
        }
        return jsonify(user_data), 200
    return jsonify({'message': 'User not found'}), 404

# Endpoint for updating user information
@app.route('/user/<email>', methods=['PUT'])
def update_user(email):
    user = User.query.get(email)
    if user:
        data = request.get_json()
        # Update user data as needed
        if 'hashed_password' in data:
            user.hashed_password = bcrypt.generate_password_hash(data['hashed_password']).decode('utf-8')
        if 'encryption_key' in data:
            user.encryption_key = data['encryption_key']
        if 'credentials' in data:
            user.credentials = encrypt_credentials(data['credentials'], user.encryption_key)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    return jsonify({'message': 'User not found'}), 404

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
@jwt_required()  # Requires a valid JWT to access the endpoint
def logout():
    jti = get_jwt_identity()['jti']
    blacklisted_tokens.add(jti)  # Add the token to the blacklist
    return jsonify({'message': 'Logout successful'}), 200

# Endpoint for retrieving and decrypting credentials
@app.route('/user/<email>/get_credentials', methods=['POST'])
@jwt_required()  # Requires a valid JWT to access the endpoint
def get_credentials(email):
    try:
        # No need to check if the token is blacklisted here, as @jwt_required() already does that
        user = User.query.get(email)
        credentials = decrypt_credentials(user.credentials, user.encryption_key)
        return jsonify({'credentials': credentials}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Endpoint for adding credentials
@app.route('/user/<email>/add_credentials', methods=['POST'])
@jwt_required()  # Requires a valid JWT to access the endpoint
def add_credentials(email):
    try:
        user = User.query.get(email)
        data = request.get_json()
        website_name = data.get('website_name')
        website_username = data.get('website_username')
        website_password = data.get('website_password')

        # Check if all required data is provided
        if not all([website_name, website_username, website_password]):
            return jsonify({'message': 'Missing required data'}), 400

        # Decrypt existing credentials
        decrypted_credentials = []
        if user.credentials:
            decrypted_credentials = json.loads(decrypt_credentials(user.credentials, user.encryption_key))

        # Add new credentials
        new_credentials = {
            'website_name': website_name,
            'website_username': website_username,
            'website_password': website_password
        }
        decrypted_credentials.append(new_credentials)

        # Encrypt updated credentials
        updated_credentials = encrypt_credentials(decrypted_credentials, user.encryption_key)

        # Convert bytes to a string before updating the user
        updated_credentials_str = updated_credentials.decode('utf-8')

        # Update user with encrypted credentials
        user.credentials = updated_credentials_str
        db.session.commit()

        return jsonify({'message': 'Credentials added successfully'}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


# Function to encrypt credentials
def encrypt_credentials(credentials, encryption_key):
    if isinstance(encryption_key, User):
        # Extract the key from the User object
        encryption_key = encryption_key.encryption_key

    # Ensure encryption_key is bytes
    encryption_key = encryption_key.encode('utf-8')

    # Convert dictionary to JSON string
    credentials_str = json.dumps(credentials)

    cipher_suite = Fernet(encryption_key)
    encrypted_credentials = cipher_suite.encrypt(credentials_str.encode('utf-8'))
    return encrypted_credentials


# Function to decrypt credentials
def decrypt_credentials(encrypted_credentials, encryption_key):
    cipher_suite = Fernet(encryption_key)
    decrypted_credentials = cipher_suite.decrypt(encrypted_credentials).decode('utf-8')
    return decrypted_credentials

def is_valid_email(email):
    # Implement your email validation logic here
    # You can use regular expressions or other methods
    # For simplicity, a basic check is implemented
    return '@' in email and '.' in email.split('@')[-1]

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)




