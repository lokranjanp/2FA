import dotenv
import redis
import mysql.connector
from mysql.connector import *
from datetime import datetime
import bcrypt
from otp import *
from otpmail import *

def hash_password(password):
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        tuple: A tuple containing the hashed password and the salt used.
    """
    user_salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), user_salt)
    return hashed_password, user_salt

def authenticate_user(stored_hash, input_password):
    """
    Authenticates a user by comparing the stored hash with the input password.

    Args:
        stored_hash (str): The hashed password stored in the database.
        input_password (str): The plain text password input by the user.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    if bcrypt.checkpw(input_password.encode('utf-8'), stored_hash.encode('utf-8')):
        print("Authentication successful")
        return True
    else:
        print("Authentication failed. Incorrect password.")
        return False

def create_connection():
    """
    Creates a connection to the MySQL database using credentials from a .env file.

    Returns:
        mysql.connector.connection.MySQLConnection: The database connection object if successful, None otherwise.
    """
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
    """
    Registers a new user by storing their details in the SQL database.

    Args:
        username (str): The username of the new user.
        email (str): The email address of the new user.
        password (str): The plain text password of the new user.

    Returns:
        bool: True if registration is successful, False otherwise.
    """
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
    """
    Validates a user by checking their username and password without 2FA.

    Args:
        username (str): The username of the user.
        password (str): The plain text password of the user.

    Returns:
        bool: True if validation is successful, False otherwise.
    """
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
    """
    Validates a user by checking their username and OTP for 2FA.

    Args:
        username (str): The username of the user.
        otp (str): The one-time password for 2FA.

    Returns:
        bool: True if validation is successful, False otherwise.
    """
    r = redis.StrictRedis(host='localhost', port=6379, db=7)

    try:
        if verify_otp(r, username, otp):
            print(f"OTP AUTH successful.")
            return True

    except Error as e:
        print(f"OTP AUTH failed.")
        return False