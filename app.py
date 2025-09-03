from flask import Flask, session, request, redirect, url_for, render_template

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to homepage.
    if session.get('logged_in'):
        return redirect(url_for('homepage'))

    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Basic login logic
        if email == 'admin@example.com' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('homepage'))
        else:
            error = 'Invalid email or password'
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if not email or not username or not password or not confirm_password:
            error = "Please fill all fields."
        elif password != confirm_password:
            error = "Passwords do not match."
        else:
            # Normally, save the new user to the database here
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.route('/homepage')
@login_required
def homepage():
    js_block = """
    <script type='text/javascript'>
        window.history.forward();
        function noBack() { window.history.forward(); }
    </script>
    """
    return js_block + render_template('Home.html')

@app.route('/form', methods=['GET', 'POST'])
@login_required
def form():
    if request.method == 'POST':
        # Process form data (fetch using request.form.get('fieldname') as per your form)
        return redirect(url_for('form_result'))
    return render_template('form.html')

@app.route('/form/result')
@login_required
def form_result():
    return render_template('result.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
