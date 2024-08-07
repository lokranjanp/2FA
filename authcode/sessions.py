import redis
import dotenv

# Session management functions using cache with Redis

path = "../.env"
r = redis.StrictRedis(host=dotenv.get_key(path, "REDIS_HOST"),
                                 port=dotenv.get_key(path, "REDIS_PORT"),
                                 db=dotenv.get_key(path, "REDIS_DB"))

def cache_login(username):
    # Cache the user's login status
    session_key = f"user_session:{username}"
    if r.setex(session_key, 1800, "active"):
        return True
    return False

def logout_user(username):
    # Remove the user's login status from the cache
    session_key = f"user_session:{username}"
    if r.delete(session_key):
        return True
    return False

def check_status(username):
    # Check if the user is logged in
    session_key = f"user_session:{username}"
    return r.exists(session_key)


def get_logged_in_users():
    # Pattern to match all user session keys
    session_pattern = "user_session:*"
    # Get all keys that match the session pattern
    session_keys = r.keys(session_pattern)
    # Extract user IDs from the session keys
    logged_in_users = [key.decode('utf-8').split(':')[1] for key in session_keys]

    return logged_in_users
