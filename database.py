from sqlite3 import Error
import hashlib
from Account import Account
from Post import Post
from Item import Item
from Request import Request
import math
from operator import itemgetter


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def hash_password(username, password):
    salt = username[:5].encode('utf-8')
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    storage = salt + key
    return storage


def salt_key(storage):
    return storage[:32], storage[32:]  # (salt, key)


def convert_to_array(str, type):
    output = None
    if len(str) != 0:
        if type == 'str':
            output = str.split(',')
        elif type == 'int':
            output = [int(x) for x in str.split(',')]
        elif type == 'bool':
            if str == 'Yes':
                output = True
            else:
                output = False
    return output


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
        insert = '''INSERT INTO accounts(name, passwd, contact, notifications, filters, posts, requests)
                    VALUES(?,?,?,?,?,?,?)'''
        values = account.get_db_array(password)
        cur.execute(insert, values)
        return True


def get_account(cur, account_id):
    cur.execute("SELECT name, contact, notifications, filters, posts, requests FROM accounts WHERE id = ?",
                [account_id])
    row = cur.fetchone()
    if row:
        name = convert_to_array(row[0], 'str')
        contact = convert_to_array(row[1], 'str')
        notifications = convert_to_array(row[2], 'bool')
        filters = convert_to_array(row[3], 'str')
        posts = convert_to_array(row[4], 'int')
        requests = convert_to_array(row[5], 'int')
        account = Account(name, contact, account_id, notifications, filters, posts, requests)
    else:
        account = None
    return account


def add_post(cur, post):
    insert = '''INSERT INTO posts(account_id, name, items, location, start_time, end_time, contact, description,
                                    logistics, tags, requests)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)'''
    values = post.get_db_array()
    cur.execute(insert, values)
    return cur.lastrowid


def get_post(cur, post_id):
    cur.execute('''
        SELECT account_id, name, items, location, start_time, end_time, contact, description, logistics, tags, requests
        FROM posts WHERE id = ?''', [post_id])
    row = cur.fetchone()
    if row:
        accountID = int(row[0])
        name = row[1]
        items = convert_to_array(row[2], 'int')
        location = convert_to_array(row[3], 'int')
        start_time = row[4]
        end_time = row[5]
        contact = row[6]
        description = row[7]
        logistics = convert_to_array(row[8], 'str')
        tags = convert_to_array(row[9], 'str')
        requests = convert_to_array(row[10], 'int')
        post = Post(name, post_id, accountID, items, location, start_time, end_time, contact, description, logistics,
                    tags, requests)
    else:
        post = None
    return post


def add_item(cur, item):
    insert = '''INSERT INTO items(account_id, post_id, name, description, tags, quantity)
                VALUES(?,?,?,?,?,?)'''
    values = item.get_db_array()
    cur.execute(insert, values)
    return cur.lastrowid


def get_item(cur, item_id):
    cur.execute('''
        SELECT account_id, post_id, name, description, tags, quantity
        FROM items WHERE id = ?''', [item_id])
    row = cur.fetchone()
    if row:
        name = row[2]
        accountID = int(row[0])
        postID = int(row[1])
        description = row[3]
        tags = convert_to_array(row[4], 'str')
        quantity = int(row[5])
        item = Item(name, accountID, postID, description, tags, quantity, item_id)
    else:
        item = None
    return item


def add_request(cur, request):
    insert = '''INSERT INTO requests(account_id, post_id, items, quantity)
                VALUES(?,?,?,?)'''
    values = request.get_db_array()
    cur.execute(insert, values)
    return cur.lastrowid


def get_request(cur, request_id):
    cur.execute('''
        SELECT account_id, post_id, items, quantity
        FROM requests WHERE id = ?''', [request_id])
    row = cur.fetchone()
    if row:
        accountID = int(row[0])
        postID = int(row[1])
        items = convert_to_array(row[2], 'int')
        quantity = convert_to_array(row[3], 'int')
        request = Request(accountID, request_id, postID, items, quantity)
    else:
        request = None
    return request


def request_post(cur, post_id, request_id):
    cur.execute('SELECT requests FROM posts WHERE id = ?', [post_id])
    requests = convert_to_array(cur.fetchone()[0], 'int')
    if requests:
        requests.append(request_id)
    else:
        requests = [request_id]
    cur.execute('UPDATE posts SET requests = ? WHERE id = ?', [','.join(str(x) for x in requests), post_id])
    return cur.lastrowid


def get_posts(cur, account, tags, location):
    posts = []
    if not tags.isEmpty():
        request = 'SELECT * FROM posts WHERE'
        for i in range(len(tags)):
            if i == len(tags) - 1:
                request = request + ' tags LIKE "%?%"'
            else:
                request = request + ' tags LIKE "%?%" OR'
        cur.execute(request, tags)
    else:
        cur.execute('SELECT * FROM posts')
    rows = cur.fetchall()
    for row in rows:
        postID = int(row[0])
        accountID = int(row[1])
        name = row[2]
        items = convert_to_array(row[3], 'int')
        location = convert_to_array(row[4], 'int')
        start_time = row[5]
        end_time = row[6]
        contact = row[7]
        description = row[8]
        logistics = convert_to_array(row[9], 'str')
        tags = convert_to_array(row[10], 'str')
        requests = convert_to_array(row[11], 'int')
        posts.append(
            Post(name, postID, accountID, items, location, start_time, end_time, contact, description, logistics, tags,
                 requests))
    for i in range(len(posts)):
        for fil in account.filters:
            if fil in posts[i].tags:
                posts.pop(i)

    sorted_posts = []
    for post in posts:
        distance = dist(location, post.location)
        sorted_posts.append((distance, post))
    sorted_posts = sorted(sorted_posts, key=itemgetter(0))

    post_id_list = []
    for post in sorted_posts:
        post_id_list.append(post[1].postID)
    return post_id_list


def init_tables(cursor):
    sql_create_accounts_table = """ CREATE TABLE IF NOT EXISTS accounts (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            passwd text NOT NULL,
                                            contact text NOT NULL,
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
                                        items text NOT NULL,
                                        quantity text NOT NULL,
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
