from flask import Flask, render_template, request
import sqlite3
import os
from config import DATABASE
from dataset import get_recommendation   # CSV function import

app = Flask(__name__)

def init_db():
    os.makedirs('database', exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  age INTEGER,
                  gender TEXT,
                  budget INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def recommend():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    budget = int(request.form['budget'])

    # CSV recommendation
    place, hotel, image = get_recommendation(budget)

    # Save user data
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO users (name,age,gender,budget) VALUES (?,?,?,?)",
              (name,age,gender,budget))
    conn.commit()
    conn.close()

    return render_template("recommend.html",
                           name=name,
                           place=place,
                           hotel=hotel,
                           image=image)
@app.route('/admin')
def admin():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return render_template("admin.html", users=users)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
