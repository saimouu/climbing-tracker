from db import db
from sqlalchemy.sql import text
import users

def get_all_climbs():
    sql = text("SELECT R.grade, R.location, R.time, R.id, U.username FROM routes R, users U WHERE R.user_id = U.id;")
    #result = db.session.execute(text("SELECT * FROM routes"))
    result = db.session.execute(sql)
    return result.fetchall()

# content is a tuple where (grade, location)
def create_climb(content: tuple):
    grade = content[0]
    location = content[1]
    user_id = users.user_id()
    if user_id != 0:        # move this check to routes
        sql = text("INSERT INTO routes (grade, location, user_id, time) VALUES (:grade, :location, :user_id, NOW())")
        db.session.execute(sql, {"grade": grade, "location": location, "user_id": user_id})
        db.session.commit()
        return True
    else:
        return False

def get_climb_by_id(id):
    #sql = text("SELECT * FROM routes WHERE routes.id = :id;")
    sql = text("SELECT R.grade, R.location, R.time, R.id, U.username FROM routes R, users U WHERE R.user_id = U.id AND R.id = :id;")
    result = db.session.execute(sql, {"id": id}).fetchone()
    return result
