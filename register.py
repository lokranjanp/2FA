import dotenv
import pyotp
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import bcrypt

def hash_password(password):
    """Returns a hashed password during user auth detail registrations"""
    user_salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), user_salt)
    return hashed_password, user_salt

def authenticate_user(stored_hash, input_password):
    # Hash the input password and compare it to the stored hash
    if bcrypt.checkpw(input_password.encode('utf-8'), stored_hash.encode('utf-8')):
        print("Authentication successful!")
        return True
    else:
        print("Authentication failed. Incorrect password.")
        return False


def create_connection():
    path = ".env"
    try:
        connection = mysql.connector.connect(
            host=dotenv.get_key(path, 'DB_HOST'),
            user=dotenv.get_key(path, 'DB_USER'),
            password=dotenv.get_key(path, 'DB_PASSWORD'),
            database=dotenv.get_key(path, 'DB_NAME')
        )
        if connection.is_connected():
            print("Successfully connected to the database")
        return connection

    except Error as e:
        print(f"Error: {e}")
        return None

def register_user(username, email, password):
    connection = create_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        created_at = datetime.now()
        user_otp_secret = pyotp.random_base32()
        hashed_password, user_salt = hash_password(password)
        cursor.execute("INSERT INTO users (username, email, password_hash, otp_secret, created_at ,user_salt) "
                       "VALUES (%s, %s, %s, %s, %s, %s)",
                       (username, email, hashed_password, user_otp_secret, created_at, user_salt))
        connection.commit()
        return True

    except Error as e:
        print(f"Error: {e}")
        return False

    finally:
        cursor.close()
        connection.close()

def validate_user(username, password):
    connection = create_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT u.password_hash, u.user_salt FROM users u WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            stored_hash, stored_salt = user
            return authenticate_user(stored_hash, password)

    except Error as e:
        print(f"Error: {e}")
        return False

    finally:
        cursor.close()
        connection.close()

print(register_user("pookie", "test@gmail.com", "password"))
print(validate_user("pookie", "password"))