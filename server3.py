from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secret key of your choice

login_manager = LoginManager(app)

# User model
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

# Returns information about users
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/login')
def login():
    user = User(user_id=1)  # Replace with your user model logic
    login_user(user)
    return 'Logged in successfully'

# Modifies current_user variable that's how it knows which user to logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully'

@app.route('/protected')
@login_required
def dashboard():
    return f'Hello, {current_user.id}!'

