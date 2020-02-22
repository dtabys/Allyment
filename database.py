import sqlite3
from sqlite3 import Error
import hashlib
import os

salt = os.urandom(32)

def hash_passwd(password):
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    storage = salt + key
    return storage

def salt_key(storage):
    return (storage[:32], storage[32:]) # (salt, key)


def create_table(cur, create_table_sql):
    try:
        cur.execute(create_table_sql)
    except Error as e:
        print(e)


def check_login(cur, user_name, password):
    password = hash_passwd(password)
    cur.execute("SELECT id FROM accounts WHERE passwd = ? AND name = ?", [password, user_name])
    account_id = cur.fetchone()
    return account_id


sql_create_accounts_table = """ CREATE TABLE IF NOT EXISTS accounts (
                                        id integer PRIMARY KEY,
                                        passwd text NOT NULL,
                                        name text NOT NULL,
                                        notifications text NOT NULL,
                                        filters text,
                                        posts text,
                                        requests text
                                    ); """

sql_create_posts_table = """CREATE TABLE IF NOT EXISTS posts (
                                    id integer PRIMARY KEY,
                                    account_id integer NOT NULL,
                                    name text NOT NULL,
                                    items text NOT NULL,
                                    location text NOT NULL,
                                    start_time integer NOT NULL,
                                    end_time integer NOT NULL,
                                    contact text NOT NULL,
                                    description text,
                                    logistics text,
                                    tags text,
                                    requests text,
                                    FOREIGN KEY (account_id) REFERENCES accounts (id)
                                );"""

sql_create_items_table = """CREATE TABLE IF NOT EXISTS items (
                                    id integer PRIMARY KEY,
                                    account_id integer NOT NULL,
                                    post_id integer NOT NULL,
                                    name text NOT NULL,
                                    description text,
                                    tags text,
                                    quantity integer NOT NULL,
                                    FOREIGN KEY (post_id) REFERENCES posts (id),
                                    FOREIGN KEY (account_id) REFERENCES accounts (id)
                                );"""

sql_create_requests_table = """CREATE TABLE IF NOT EXISTS requests (
                                    id integer PRIMARY KEY,
                                    account_id integer NOT NULL,
                                    post_id integer NOT NULL,
                                    request_items text NOT NULL,
                                    request_quantity integer NOT NULL,
                                    FOREIGN KEY (post_id) REFERENCES posts (id),
                                    FOREIGN KEY (account_id) REFERENCES accounts (id)
                                );"""

def init_tables(cursor):
    if cursor is not None:
        # create tables
        create_table(cursor, sql_create_accounts_table)
        create_table(cursor, sql_create_posts_table)
        create_table(cursor, sql_create_items_table)
        create_table(cursor, sql_create_requests_table)
    else:
        print("Error! cannot create the database connection.")