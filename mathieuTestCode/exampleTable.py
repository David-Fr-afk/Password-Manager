from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PickleType

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_logged_in = db.Column(db.Boolean, default=False)
    encryption_key = db.Column(db.String(255))  # You may need to adjust the length

    # New columns to store encrypted groups of website information
    saved_groups = db.Column(PickleType)
    encrypted_website_info = db.Column(PickleType)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_logged_in = False
        self.encryption_key = generate_encryption_key()  # Define a function to generate keys

    def decrypt_groups(self):
        # Implement decryption logic using the encryption key
        # Example: decrypt(self.saved_groups, self.encryption_key)
        pass

    def encrypt_groups(self, groups_data):
        # Implement encryption logic using the encryption key
        # Example: encrypt(groups_data, self.encryption_key)
        pass

    def decrypt_website_info(self):
        # Implement decryption logic using the encryption key
        # Example: decrypt(self.encrypted_website_info, self.encryption_key)
        pass

    def encrypt_website_info(self, website_info):
        # Implement encryption logic using the encryption key
        # Example: encrypt(website_info, self.encryption_key)
        pass

    # The encryption key is also hashed to ensure it's not stored in plain text 