from db import db
from sqlalchemy.sql import text
import users

def add_comment(content: tuple):
    comment = content[0]
    route_id = content[1]
    user_id = users.user_id()
    
    if user_id != 0 and len(comment) > 3:
        sql = text("INSERT INTO comments (content, user_id, route_id, time, visible) VALUES (:content, :user_id, :route_id, NOW(), TRUE)")
        db.session.execute(sql, {"content": comment, "user_id": user_id, "route_id": route_id})
        db.session.commit()
        return True
    else:
        return False

def get_comments_by_climb(id):
    sql = """SELECT C.content, C.id, C.user_id, C.route_id, C.time, U.username FROM comments C, users U WHERE U.id=C.user_id 
    AND C.route_id=:id AND C.visible=TRUE ORDER BY C.time DESC;"""
    result = db.session.execute(text(sql), {"id": id}).fetchall()
    return result

def get_user_comments(user_id):
    sql = """SELECT C.content, C.user_id, C.route_id, C.time, U.username FROM comments C, users U WHERE U.id=C.user_id 
    AND U.id=:user_id AND C.visible=TRUE;"""
    result = db.session.execute(text(sql), {"user_id": user_id}).fetchall()
    return result

def get_comment_user(id):
    sql = text("SELECT user_id FROM comments WHERE id=:id")
    result = db.session.execute(sql, {"id": id}).fetchone()
    return result[0]

def get_comment_climb(id):
    sql = text("SELECT route_id FROM comments WHERE id=:id;")
    result = db.session.execute(sql, {"id": id}).fetchone()
    return result[0]

def remove_comment(id):
    sql = text("UPDATE comments SET visible=FALSE WHERE id=:id;")
    if users.user_id() == get_comment_user(id):
        db.session.execute(sql, {"id": id})
        db.session.commit()
        return True
    return False

