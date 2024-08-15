from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
import dotenv
from authcode import sessions, register, otp, otpmail

app = Flask(__name__)
app.secret_key = dotenv.get_key('.env', 'SECRET_KEY')

@app.route('/')
def home():
    login()
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect to dashboard if already logged in
    user_mail = request.form['email']
    user_password = request.form['password']
    username = request.form['username']
    if sessions.check_status(username):
        return redirect(url_for('dashboard'))
    else:
        if request.method == 'POST':
            if register.validate_user(user_mail, user_password):
                sessions.cache_login(username)
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password. Please try again.', 'danger')

    # Set cache control headers to prevent caching of the login page
    response = make_response(render_template('login.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    return f"Welcome to your dashboard, {session['email']}!"

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
