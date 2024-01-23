from flask import Flask, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_hex  # Import the 'secrets' module for secure random generation
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wefsdfsdfgrea*&YB#*BDNS'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

db = SQLAlchemy(app)
login_manager = LoginManager(app)

CORS(app, supports_credentials=True)  

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)  # Increase the length
    salt = db.Column(db.String(16), nullable=False)
    credentials = db.Column(db.JSON, default={})

# Returns user id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    # Generate a random salt
    salt = token_hex(8)  # 16 characters (8 bytes)

    # Combine the password and salt, then hash
    hashed_password = generate_password_hash(password + salt, method='pbkdf2:sha256')

    new_user = User(email=email, hashed_password=hashed_password, salt=salt)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    # Adds the user's unique salt to their hashed password
    if user and check_password_hash(user.hashed_password, password + user.salt):
        login_user(user, remember=True)  # or login_user(user, remember=False) for a session until browser close
        return jsonify({'message': 'Logged in successfully'})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
@app.route('/save_credentials', methods=['POST'])
@login_required
def save_credentials():
    data = request.get_json()
    website = data.get('website')
    username = data.get('username')
    password = data.get('password')

    # Encrypt the password using the user's unique salt
    encrypted_password = generate_password_hash(password + current_user.salt, method='pbkdf2:sha256')

    # Retrieve existing credentials
    user_credentials = current_user.credentials.copy()

    # Update or add the new credentials to the dictionary
    user_credentials[website] = {'username': username, 'password': encrypted_password}

    # Update the User model with the modified credentials
    current_user.credentials = user_credentials
    db.session.commit()

    return jsonify({'message': 'Credentials saved successfully'})

@app.route('/view_credentials', methods=['GET'])
@login_required
def view_credentials():
    return jsonify(current_user.credentials)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

