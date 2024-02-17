from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            return True
        else:
            return False

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password, admin) VALUES (:username, :password, FALSE)")
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["user_id"]

def user_id():
    return session.get("user_id", 0)

def is_admin():
    sql = text("SELECT admin FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id": user_id()})
    return result

def get_name_by_id(id):
    sql = text("SELECT username FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone().username

def valid_register(username, password):
    if len(password) < 6 or len(username) < 3:
        return False
    return True
