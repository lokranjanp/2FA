import dotenv
import redis
import mysql.connector
from mysql.connector import *
from datetime import datetime
import bcrypt
from otp import *
from otpmail import *

def hash_password(password):
    """Returns a hashed password during user auth detail registrations"""
    user_salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), user_salt)
    return hashed_password, user_salt

def authenticate_user(stored_hash, input_password):
    """Authenticates the user during login"""
    # Hash the input password and compare it to the stored hash
    if bcrypt.checkpw(input_password.encode('utf-8'), stored_hash.encode('utf-8')):
        print("Authentication successful")
        return True
    else:
        print("Authentication failed. Incorrect password.")
        return False

def create_connection():
    """Creates a connection to the MySQL database"""
    path = "../.env"
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
        print(f"Database Connection FAILED. Error: {e}")
        return None

def register_user(username, email, password):
    """Registers a user and stores the data in the SQL Database"""
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
        print(f"Registration Failed. Error: {e}")
        return False

    finally:
        cursor.close()
        connection.close()

def validate_user(username, password):
    """User validation without 2FA"""
    connection = create_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT u.password_hash, u.user_salt FROM users u WHERE u.username = %s", (username,))
        user = cursor.fetchone()

        if user:
            stored_hash, stored_salt = user
            return authenticate_user(stored_hash, password)

    except Error as e:
        print(f"Password auth failed. Error: {e}")
        return False

    finally:
        cursor.close()
        connection.close()

def validate_user_2FA(username, otp):
    """User validation with 2FA"""
    r = redis.StrictRedis(host='localhost', port=6379, db=7)

    try:
        if verify_otp(r, username, otp):
            print(f"OTP AUTH successful.")
            return True

    except Error as e:
        print(f"OTP AUTH failed.")
        return False
