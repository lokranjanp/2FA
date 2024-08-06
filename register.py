import dotenv
import pyotp
import mysql.connector
from mysql.connector import Error
from hashlib import sha256
from datetime import datetime

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
        hashed_password = sha256(password.encode('utf-8')).hexdigest()
        cursor.execute("INSERT INTO users (username, email, password_hash, otp_secret, created_at) "
                       "VALUES (%s, %s, %s, %s, %s)", (username, email, hashed_password, user_otp_secret, created_at))
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
        cursor.execute("SELECT u.password_hash FROM users u WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user is None:
            return False

        hashed_password = sha256(password.encode('utf-8')).hexdigest()
        if user[0] == hashed_password:
            return True

        return False

    except Error as e:
        print(f"Error: {e}")
        return False

    finally:
        cursor.close()
        connection.close()

