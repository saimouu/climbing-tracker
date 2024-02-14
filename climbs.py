from db import db
from sqlalchemy.sql import text
import users

def get_all_climbs():
    sql = text("SELECT R.grade, R.location, R.time, R.id, U.username, R.user_id FROM routes R, users U WHERE R.user_id = U.id AND R.visible=TRUE ORDER BY R.time DESC;")
    result = db.session.execute(sql)
    return result.fetchall()

def check_climb_content(content):
    if len(content["grade"]) < 1 or len(content["location"]) < 2:
        return False
    return True

def create_climb(content):
    # TODO: different error message
    if not check_climb_content(content=content):
        return False
    grade = content["grade"]
    location = content["location"]
    indoor = content["indoor"]
    flash = content["flash"]
    user_id = users.user_id()
    if user_id != 0:       
        sql = """INSERT INTO routes (grade, location, user_id, time, visible, indoor) 
        VALUES (:grade, :location, :user_id, NOW(), TRUE, :indoor) RETURNING id"""
        temp_id_object = db.session.execute(text(sql), {"grade": grade, "location": location, "user_id": user_id, "indoor": indoor})
        db.session.commit()
        route_id = temp_id_object.fetchone().id
        if add_flash_data(user_id=user_id, route_id=route_id, flash=flash):
            return True
    else:
        return False

def get_climb_by_id(id):
    sql = text("SELECT R.grade, R.location, R.time, R.id, R.user_id, U.username FROM routes R, users U WHERE R.user_id = U.id AND R.id = :id;")
    result = db.session.execute(sql, {"id": id}).fetchone()
    return result

def get_climbs_by_user(id):
    sql = text("SELECT R.grade, R.location, R.time, R.id, U.username FROM routes R, users U WHERE U.id = R.user_id AND R.user_id = :id AND R.visible = TRUE ORDER BY R.time DESC;")
    result = db.session.execute(sql, {"id": id}).fetchall()
    return result

def delete_climb(id):
    sql = text("UPDATE routes SET visible=FALSE WHERE id=:id;")
    if users.user_id() == get_climb_by_id(id).user_id:
        db.session.execute(sql, {"id": id})
        db.session.commit()
        return True
    return False

def get_users_hardest_climb(user_id):
    sql = text("SELECT R.grade, R.time FROM routes R, users U WHERE R.user_id=U.id and U.id=:user_id AND R.visible=True ORDER BY R.grade DESC;")
    result = db.session.execute(sql, {"user_id": user_id}).fetchone()
    return result

def add_flash_data(route_id, user_id, flash):
    try:
        sql = text("INSERT INTO flashes (route_id, user_id, flash) VALUES (:route_id, :user_id, :flash)")
        db.session.execute(sql, {"route_id": route_id, "user_id": user_id, "flash": flash})
        db.session.commit()
        return True
    except:
        return False

# user_id is optional parameter. if not given counts all climbs
def amount_of_climbs(user_id=0):
    if user_id == 0:
        sql = text("SELECT COUNT(*) FROM routes R, users U WHERE R.user_id = U.id AND R.visible=TRUE;")
        result = db.session.execute(sql)
    else:
        sql = text("SELECT COUNT(*) FROM routes R, users U WHERE R.user_id = U.id AND R.visible=TRUE AND R.user_id=:user_id;")
        result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchone()[0]