from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('gcs_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            date_of_assessment TEXT,
            examiner_name TEXT,
            eye_response INTEGER,
            verbal_response INTEGER,
            motor_response INTEGER,
            total_score INTEGER,
            comments TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    age = int(request.form.get('age'))
    gender = request.form.get('gender')
    date_of_assessment = request.form.get('date_of_assessment')
    examiner_name = request.form.get('examiner_name')
    eye_response = int(request.form.get('eye_response'))
    verbal_response = int(request.form.get('verbal_response'))
    motor_response = int(request.form.get('motor_response'))
    comments = request.form.get('comments')

    # Calculate total score
    total_score = eye_response + verbal_response + motor_response

    # Save data to the database
    conn = sqlite3.connect('gcs_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO responses (name, age, gender, date_of_assessment, examiner_name, eye_response, verbal_response, motor_response, total_score, comments)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, age, gender, date_of_assessment, examiner_name, eye_response, verbal_response, motor_response, total_score, comments))
    conn.commit()
    conn.close()

    return redirect(url_for('thank_you', score=total_score))

@app.route('/thank_you')
def thank_you():
    score = request.args.get('score')
    return render_template('thank_you.html', score=score)

@app.route('/report')
def report():
    conn = sqlite3.connect('gcs_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM responses')
    data = cursor.fetchall()
    conn.close()
    return render_template('report.html', data=data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
