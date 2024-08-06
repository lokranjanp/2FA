from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mail import Mail, Message
import bcrypt
import random
import os

app = Flask(__name__)
app.secret_key = os.get_key('SECRET_KEY')

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
