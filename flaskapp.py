from flask import Flask, render_template, request, redirect, url_for

import sqlite3

import os



app = Flask(__name__)



# SQLite setup

DATABASE = 'users.db'



def init_db():

    conn = sqlite3.connect(DATABASE)

    c = conn.cursor()

    c.execute('''

    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT NOT NULL,

        password TEXT NOT NULL,

        firstname TEXT,

        lastname TEXT,

        email TEXT,

        file_name TEXT,

        word_count INTEGER

    );

    ''')

    conn.commit()

    conn.close()



init_db()



@app.route('/')

def index():

    message = request.args.get('message')  # Get the message from query parameters

    return render_template('register.html', message=message)



@app.route('/register', methods=['POST'])

def register():

    username = request.form['username']

    password = request.form['password']

    firstname = request.form['firstname']

    lastname = request.form['lastname']

    email = request.form['email']

    file = request.files['file']



    if file:
         file_name = file.filename

        file.save(os.path.join('uploads', file_name))

        word_count = count_words(os.path.join('uploads', file_name))

    else:

        file_name = None

        word_count = 0



    conn = sqlite3.connect(DATABASE)

    c = conn.cursor()

    c.execute("INSERT INTO users (username, password, firstname, lastname, email, file_name, word_count) VALUES (?, ?, ?, ?, ?, ?, ?)",

              (username, password, firstname, lastname, email, file_name, word_count))

    conn.commit()

    conn.close()



    return redirect(url_for('index', message="You have successfully registered."))



@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']



        conn = sqlite3.connect(DATABASE)

        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))

        user = c.fetchone()

        conn.close()



        if user:

            return render_template('profile.html', user=user)

        else:

            return "Invalid credentials. Please try again."



    return render_template('login.html')



@app.route('/download/<filename>')

def download_file(filename):

    return send_file(os.path.join('uploads', filename), as_attachment=True)



def count_words(file_path):

    with open(file_path, 'r') as file:
        content = file.read()

        return len(content.split())



if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)