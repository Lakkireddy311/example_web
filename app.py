from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="login"
)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        mail_id = request.form['mail_id']
        password = request.form['password']

        cursor = db.cursor()
        query = "SELECT * FROM login WHERE mail_id = %s AND password = %s"
        cursor.execute(query, (mail_id, password))  # Fixed variable mismatch
        result = cursor.fetchone()

        if result:
            return "Login successful!"
        else:
            return "Invalid email or password."

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        mail_id = request.form['mail_id']
        phone_number = request.form['phone_number']
        password = request.form['password']

        # Create cursor and ensure table exists
        cursor = db.cursor()

        # Create a table if it doesn't exist
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS login (
                username VARCHAR(255),
                mail_id VARCHAR(255),
                phone_number VARCHAR(255),
                password VARCHAR(255)
            )
        '''
        cursor.execute(create_table_query)

        # Insert the data into the database
        insert_query = '''
            INSERT INTO login (username, mail_id, phone_number, password)
            VALUES (%s, %s, %s, %s)
        '''
        insert_values = (username, mail_id, phone_number, password)
        cursor.execute(insert_query, insert_values)
        db.commit()

        return "Sign-up successful!"

    return render_template('signup.html')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
