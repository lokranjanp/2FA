from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy user data (in a real application, use a database)
users = {
    "user@example.com": {
        "password": "password123"
    }
}

@app.route('/', methods=['GET', 'POST'])
def login():
    # Redirect to dashboard if already logged in
    if 'email' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users.get(email)
        if user and user['password'] == password:
            session['email'] = email
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')

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
