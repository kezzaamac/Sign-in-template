
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for sessions

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with open('records.txt', 'r') as file:
            for line in file:
                stored_info = line.strip().split(',')
                if len(stored_info) >= 2 and stored_info[0].strip() == f"Username: {username}" and stored_info[1].strip() == f"Password: {password}":
                    session['logged_in'] = True
                    session['username'] = username
                    return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with open('records.txt', 'a') as file:
            file.write(f"Username: {username}, Password: {password}\n")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')

@app.route('/')
def home():
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
