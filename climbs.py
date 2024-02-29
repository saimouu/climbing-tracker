from sqlalchemy.sql import text
from db import db
import users
import flashes

def get_all_climbs():
    sql = """
        SELECT R.grade, R.location, R.time, R.id, U.username, R.user_id, R.indoor 
        FROM routes R, users U 
        WHERE R.user_id = U.id AND R.visible=TRUE ORDER BY R.time DESC;
    """
    result = db.session.execute(text(sql))
    return result.fetchall()

def check_climb_content(content):
    if 3 <= len(content["location"]) <= 100:
        return True
    return False

def create_climb(content):
    grade, location = content["grade"], content["location"]
    indoor, flash = content["indoor"], content["flash"]
    user_id = users.user_id()
    if user_id != 0:
        sql = """
            INSERT INTO routes (grade, location, user_id, time, visible, indoor) 
            VALUES (:grade, :location, :user_id, NOW(), TRUE, :indoor) 
            RETURNING id;
        """
        temp_id_object = db.session.execute(text(sql), {"grade": grade, "location": location,
         "user_id": user_id, "indoor": indoor})
        db.session.commit()
        route_id = temp_id_object.fetchone().id
        if flashes.add_flash_data(user_id=user_id, route_id=route_id, flash=flash):
            return (True, route_id)
    else:
        return (False, 0)

def get_climb_by_id(id):
    sql = """
        SELECT R.grade, R.location, R.time, R.id, R.user_id, U.username 
        FROM routes R, users U 
        WHERE R.user_id = U.id AND R.id = :id;
    """
    result = db.session.execute(text(sql), {"id": id}).fetchone()
    return result

def get_climbs_by_user(id):
    sql = """
        SELECT R.grade, R.location, R.time, R.id, U.username, U.id AS user_id 
        FROM routes R, users U WHERE U.id = R.user_id AND R.user_id = :id AND R.visible=TRUE 
        ORDER BY R.time DESC;
    """
    result = db.session.execute(text(sql), {"id": id}).fetchall()
    return result

def delete_climb(id):
    sql = "UPDATE routes SET visible=FALSE WHERE id=:id;"
    if users.user_id() == get_climb_by_id(id).user_id:
        db.session.execute(text(sql), {"id": id})
        db.session.commit()
        return True
    return False

def get_users_hardest_climb(user_id):
    sql = """
        SELECT R.grade, R.time FROM routes R, users U 
        WHERE R.user_id=U.id AND U.id=:user_id AND R.visible=True 
        ORDER BY R.grade DESC;
    """
    result = db.session.execute(text(sql), {"user_id": user_id}).fetchone()
    return result

# user_id is optional parameter. if not given counts all climbs
def amount_of_climbs(user_id=0):
    if user_id == 0:
        sql = """
            SELECT COUNT(*) FROM routes R, users U 
            WHERE R.user_id = U.id AND R.visible=TRUE;
        """
        result = db.session.execute(text(sql))
    else:
        sql = """
            SELECT COUNT(*) FROM routes R, users U 
            WHERE R.user_id = U.id AND R.visible=TRUE AND R.user_id=:user_id;
        """
        result = db.session.execute(text(sql), {"user_id": user_id})
    return result.fetchone()[0]

def valid_grades():
    font_scale = ["4", "5", "5+", "6a", "6a+", "6b", "6b+", "6c", "6c+",
    "7a", "7a+", "7b", "7b+", "7c", "7c+", "8a", "8a+", "8b", "8b+", "8c", "8c+", "9a"]
    return font_scale

def get_user_grade_distribution(user_id):
    sql = """
        SELECT grade, COUNT(*) FROM routes 
        WHERE user_id=:user_id AND visible=TRUE 
        GROUP BY grade ORDER BY grade;"""
    result = db.session.execute(text(sql), {"user_id": user_id}).fetchall()
    return result
