from flask import Flask, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

database = sqlite3.connect("data/database.db")
database.row_factory = sqlite3.Row
db_cursor = database.cursor()

@app.route("/")
def index():
    pass

@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name") if request.form.get("name") else False
        password = request.form.get("password") if request.form.get("password") else False
        pass
    else
        pass

if __name__ == '__main__':
    app.run("127.0.0.1", "8000")
