from otp import *
from otpmail import *
from register import *
from sessions import *

def validate_input(validator, type):
    return True

print("Registration : \n")
username = str(input("Enter your Username : "))
useremail = str(input("Enter your Email : "))
userpassword = str(input("Enter your Password : "))

if (validate_input(validator=username, type="stringmix1") and validate_input(validator=useremail, type="stringmail")
        and validate_input(validator=userpassword, type="stringmix2")):
    if register_user(username, useremail, userpassword):
        print("Registration Successful")
