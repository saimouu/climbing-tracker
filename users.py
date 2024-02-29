from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username;"
    result = db.session.execute(text(sql), {"username": username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = username
        return True
    return False

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = """
            INSERT INTO users (username, password, admin) 
            VALUES (:username, :password, FALSE)
        """
        db.session.execute(text(sql), {"username": username, "password": hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["user_id"]

def user_id():
    return session.get("user_id", 0)

def is_admin():
    sql = "SELECT admin FROM users WHERE id=:id;"
    result = db.session.execute(text(sql), {"id": user_id()})
    return result

def get_name_by_id(id):
    sql = "SELECT username FROM users WHERE id=:id;"
    result = db.session.execute(text(sql), {"id": id})
    return result.fetchone().username

def valid_register(username, password):
    if len(password) < 6 or len(username) < 3:
        return False
    return True
