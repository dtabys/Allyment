from flask import Flask, request, session
import sqlite3
import random
import string
from sqlite3 import Error
import json
from database import init_tables, check_login, register_account, get_account, get_post
from Account import Account

app = Flask(__name__)

database = sqlite3.connect("data/database.db")
database.row_factory = sqlite3.Row

SESSION_TYPE = 'memcached'
app.secret_key = "TEST SECRET KEY CHANGE BEFORE DEPLOYMENT"

@app.route("/")
def index():
    response = {"status": "error", "reason": "invalid path"}
    return json.dumps(response)


@app.route("/register", methods=["POST"])
def register():
    with sqlite3.connect("data/database.db") as database:
        response = {}
        cursor = database.cursor()
        session.clear()

        if (request.is_json):
            content = request.get_json()
            if (content["username"] and content["password"]):
                account = Account(content["username"])
                if (register_account(cursor, account, content["password"])):
                    response["status"] = "success"
                else:
                    response["status"] = "error"
                    response["reason"] = "registeration failed"
            else:
                response["status"] = "error"
                response["reason"] = "missing username or password"
        else:
            response["status"] = "error"
            response["reason"] = "Invalid JSON"

        database.commit()
        cursor.close()
        return json.dumps(response)


@app.route("/login", methods=["POST"])
def login():
    with sqlite3.connect("data/database.db") as database:
        response = {}
        cursor = database.cursor()
        session.clear()

        if (request.is_json):
            content = request.get_json()
            if (content["username"] and content["password"]):
                accountId = check_login(cursor, content["username"], content["password"])
                if (accountId is None):
                    response["status"] = "unauthorized"
                    response["reason"] = "username or password incorrect"
                else:
                    response["status"] = "success"
                    response["result"] = {"accountId" : accountId}
                    session["accountId"] = accountId
                    session["loggedin"] = True
                    session["username"] = content["username"]
            else:
                response["status"] = "error"
                response["reason"] = "missing username or password"
        else:
            response["status"] = "error"
            response["reason"] = "Invalid JSON"

        database.commit()
        cursor.close()
        return json.dumps(response)


@app.route("/accinfo", methods=["POST"])
def accinfo():
    with sqlite3.connect("data/database.db") as database:
        cursor = database.cursor()
        response = {}
        if (request.is_json):
            if (session.get("loggedin")):
                content = request.get_json()
                if(content["accountId"]):
                    if(content["accountId"] == session.get("accountId")):
                        account = get_account(cursor, content["accountId"])
                        if(account):
                            response["status"] = "success"
                            response["result"] = account.__dict__
                        else:
                            response["status"] = "notfound"
                            response["reason"] = "account not found"
                    else:
                        response["status"] = "unauthorized"
                        response["reason"] = "access denied"
                else:
                    response["status"] = "incomplete"
                    response["reason"] = "accountid missing"
            else:
                response["status"] = "unauthorized"
                response["reason"] = "not logged in"
        else:
            response["status"] = "error"
            response["reason"] = "Invalid JSON"

    database.commit()
    cursor.close()
    database.close()
    return json.dumps(response)

@app.route("/getpost", methods=["POST"])
def getpost():
    with sqlite3.connect("data/database.db") as database:
        cursor = database.cursor()
        response = {}
        if (request.is_json):
            if (session.get("loggedin")):
                content = request.get_json()
                if(content["postId"]):
                    post = get_post(cursor, content["postId"])
                    if(post):
                        response["status"] = "success"
                        response["result"] = post.__dict__
                    else:
                        response["status"] = "notfound"
                        response["reason"] = "post not found"
                else:
                    response["status"] = "incomplete"
                    response["reason"] = "postid missing"
            else:
                response["status"] = "unauthorized"
                response["reason"] = "not logged in"
        else:
            response["status"] = "error"
            response["reason"] = "Invalid JSON"

    database.commit()
    cursor.close()
    database.close()
    return json.dumps(response)



if __name__ == '__main__':
    with sqlite3.connect("data/database.db") as database:
        dbcur = database.cursor()
        init_tables(dbcur)
        database.commit()
        dbcur.close()
        database.close()
        app.run("127.0.0.1", "8000")
