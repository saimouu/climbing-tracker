from db import db
from sqlalchemy.sql import text
import users

def add_comment(content: tuple):
    comment = content[0]
    route_id = content[1]
    user_id = users.user_id()
    
    if user_id != 0 and len(comment) > 3:
        sql = text("INSERT INTO comments (content, user_id, route_id, time) VALUES (:content, :user_id, :route_id, NOW())")
        db.session.execute(sql, {"content": comment, "user_id": user_id, "route_id": route_id})
        db.session.commit()
        return True
    else:
        return False

def get_comments_by_climb(id):
    sql = text("SELECT C.content, C.user_id, C.route_id, C.time, U.username FROM comments C, users U WHERE U.id = C.user_id AND C.route_id = :id ORDER BY C.time DESC;")
    result = db.session.execute(sql, {"id": id}).fetchall()
    return result

def get_user_comments(user_id):
    sql = text("SELECT C.content, C.user_id, C.route_id, C.time, U.username FROM comments C, users U WHERE U.id = C.user_id AND U.id = :user_id;")
    result = db.session.execute(sql, {"user_id": user_id}).fetchall()
    return result
