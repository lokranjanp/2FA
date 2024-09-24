import redis
import dotenv

# Session management functions using cache with Redis

# Load environment variables from .env file
path = "../.env"
r = redis.StrictRedis(host=dotenv.get_key(path, "REDIS_HOST"),
                      port=dotenv.get_key(path, "REDIS_PORT"),
                      db=dotenv.get_key(path, "REDIS_DB"))

def cache_login(username):
    """
    Cache the user's login status.

    Args:
        username (str): The username of the user.

    Returns:
        bool: True if the login status was successfully cached, False otherwise.
    """
    session_key = f"user_session:{username}"
    if r.setex(session_key, 1800, "active"):
        return True
    return False

def logout_user(username):
    """
    Remove the user's login status from the cache.

    Args:
        username (str): The username of the user.

    Returns:
        bool: True if the login status was successfully removed, False otherwise.
    """
    session_key = f"user_session:{username}"
    if r.delete(session_key):
        return True
    return False

def check_status(username):
    """
    Check if the user is logged in.

    Args:
        username (str): The username of the user.

    Returns:
        bool: True if the user is logged in, False otherwise.
    """
    session_key = f"user_session:{username}"
    return r.exists(session_key)

def get_logged_in_users():
    """
    Get a list of all logged-in users.

    Returns:
        list: A list of usernames of all logged-in users.
    """
    session_pattern = "user_session:*"
    session_keys = r.keys(session_pattern)
    logged_in_users = [key.decode('utf-8').split(':')[1] for key in session_keys]

    return logged_in_users