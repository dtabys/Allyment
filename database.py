from sqlite3 import Error
import hashlib
from Account import Account
from Post import Post


def hash_password(username, password):
    salt = username[:5].encode('utf-8')
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    storage = salt + key
    return storage


def salt_key(storage):
    return storage[:32], storage[32:]  # (salt, key)


def create_table(cur, create_table_sql):
    try:
        cur.execute(create_table_sql)
    except Error as e:
        print(e)


def check_login(cur, username, password):
    password = hash_password(username, password)
    cur.execute("SELECT id FROM accounts WHERE passwd = ? AND name = ?", [password, username])
    account_id = cur.fetchone()
    if account_id:
        return account_id[0]
    else:
        return None


def register_account(cur, account, password):
    username = account.getName()
    cur.execute("SELECT id FROM accounts WHERE name = ?", [username])
    exists = cur.fetchone()
    if exists:
        return False
    else:
        password = hash_password(username, password)
        insert = '''INSERT INTO accounts(name, passwd, notifications, filters, posts, requests)
                    VALUES(?,?,?,?,?,?)'''
        values = account.get_db_array(password)
        cur.execute(insert, values)
        return True


def get_account(cur, account_id):
    cur.execute("SELECT name, notifications, filters, posts, requests FROM accounts WHERE id = ?", [account_id])
    row = cur.fetchone()
    if row:
        account = Account(account_id, row[0], row[1], row[2], row[3], row[4])
    else:
        account = None
    return account


def add_post(cur, post):
    insert = '''INSERT INTO posts(account_id, name, items, location, start_time, end_time, contact, description,
                                    logistics, tags, requests)
                VALUES(?,?,?,?,?,?)'''
    values = post.get_db_array()
    return cur.lastrowid


def get_post(cur, post_id):
    cur.execute('''
        SELECT account_id, name, items, location, start_time, end_time, contact, description, logistics, tags, requests
        FROM posts WHERE id = ?''',
                [post_id])
    row = cur.fetchone()
    if row:
        account = Post(post_id, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
    else:
        account = None
    return account


def init_tables(cursor):
    sql_create_accounts_table = """ CREATE TABLE IF NOT EXISTS accounts (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            passwd text NOT NULL,
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

    if cursor is not None:
        # create tables
        create_table(cursor, sql_create_accounts_table)
        create_table(cursor, sql_create_posts_table)
        create_table(cursor, sql_create_items_table)
        create_table(cursor, sql_create_requests_table)
    else:
        print("Error! cannot create the database connection.")
