import redis
import dotenv

# Session management functions using cache with Redis

path = ".env"
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

