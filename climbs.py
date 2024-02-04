from db import db
from sqlalchemy.sql import text
import users

def get_all_climbs():
    sql = text("SELECT R.grade, R.location, R.time, R.id, U.username, R.user_id FROM routes R, users U WHERE R.user_id = U.id AND R.visible=TRUE;")
    result = db.session.execute(sql)
    return result.fetchall()

# content is a tuple where (grade, location)
def create_climb(content: tuple):
    grade = content[0]
    location = content[1]
    user_id = users.user_id()
    if user_id != 0:       
        sql = text("INSERT INTO routes (grade, location, user_id, time, visible) VALUES (:grade, :location, :user_id, NOW(), TRUE)")
        db.session.execute(sql, {"grade": grade, "location": location, "user_id": user_id})
        db.session.commit()
        return True
    else:
        return False

def get_climb_by_id(id):
    sql = text("SELECT R.grade, R.location, R.time, R.id, R.user_id, U.username FROM routes R, users U WHERE R.user_id = U.id AND R.id = :id;")
    result = db.session.execute(sql, {"id": id}).fetchone()
    return result

def get_climbs_by_user(id):
    sql = text("SELECT R.grade, R.location, R.time, R.id, U.username FROM routes R, users U WHERE U.id = R.user_id AND R.user_id = :id AND R.visible = TRUE;")
    result = db.session.execute(sql, {"id": id}).fetchall()
    return result

def delete_climb(id):
    sql = text("UPDATE routes SET visible=FALSE WHERE id=:id;")
    if users.user_id() == get_climb_by_id(id).user_id:
        db.session.execute(sql, {"id": id})
        db.session.commit()
        return True
    return False
