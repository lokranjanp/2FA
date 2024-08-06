import bcrypt

def hash_password(password):
    """Returns a hashed password during user auth detail registrations"""
    user_salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), user_salt)
    return hashed_password

def check_password(password, hashed_password):
    """Returns a boolean value to check if the password is correct"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
