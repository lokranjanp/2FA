import pyotp
import random
import json

def generate_otp(user_secret):
    """
    Generates a one-time password (OTP) for a user using their stored secret key.

    Args:
        user_secret (str): The secret key stored for the user.

    Returns:
        str: The generated OTP.
    """
    counter = random.randint(0, 696969)
    hotp = pyotp.HOTP(user_secret)
    return hotp.at(counter)

def cache_otp(r, username, otp):
    """
    Caches the OTP and username in Redis.

    Args:
        r (redis.StrictRedis): The Redis connection object.
        username (str): The username of the user.
        otp (str): The generated OTP.

    Returns:
        None
    """
    user_data = {
        "otp": otp,
        "username": username
    }
    r.setex(f'otp:{username}', 300, json.dumps(user_data))

def verify_otp(r, username, input_otp):
    """
    Verifies the OTP against the cached one in Redis.

    Args:
        r (redis.StrictRedis): The Redis connection object.
        username (str): The username of the user.
        input_otp (str): The OTP input by the user.

    Returns:
        bool: True if the OTP is valid, False otherwise.
    """
    otp_data_json = r.get(f'otp:{username}')
    if otp_data_json:
        otp_data = json.loads(otp_data_json)
        cached_otp = otp_data["otp"]

        if cached_otp == input_otp:
            # Log it as a success
            r.delete(f'otp:{username}')
            return True
        else:
            # Log it as a failure
            return False
    else:
        print("No OTP found in cache.")
        return False