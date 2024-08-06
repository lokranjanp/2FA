import pyotp
import redis
import smtplib
import random
import json
from email.mime.text import MIMEText

# fetch user secret from mysql

def generate_otp(user_secret):
    counter = random.randint(0, 696969)
    hotp = pyotp.HOTP(user_secret)
    return hotp.at(counter), counter

def cache_otp(r, username, otp, counter):
    user_data = {
        "otp": otp,
        "counter": counter,
        "username": username,
        "status": "pending"
    }

    r.setex(f'otp:{username}', 10, json.dumps(user_data))

def verify_otp(r, username, input_otp):
    otp_data_json = r.get(f'otp:{username}')
    if otp_data_json:
        otp_data = json.loads(otp_data_json)
        if otp_data == input_otp:
            # log it as a success
            r.delete(f'otp:{username}')
            return True
        else:
            # log it as a failure
            return False

r = redis.StrictRedis(host='localhost', port=6379, db=7)
cache_otp(r, 'pookie', 696969, 2)
