from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Import the 'text' function

app = Flask(__name__)

# Replace the following with your actual database connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Test route for checking the database connection
@app.route('/test_connection')
def test_connection():
    try:
        # Use the 'text' function to explicitly declare the SQL expression
        db.session.execute(text('SELECT 1'))
        return 'Database connection successful!'
    except Exception as e:
        return f'Database connection error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)