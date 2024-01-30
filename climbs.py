from db import db
from sqlalchemy.sql import text
import users

def get_all_climbs():
    result = db.session.execute(text("SELECT * FROM routes"))
    return result.fetchall()

# content is a tuple where (grade, location)
def create_climb(content: tuple):
    grade = content[0]
    location = content[1]
    user_id = users.user_id()
    if user_id != 0:
        sql = text("INSERT INTO routes (grade, location, user_id) VALUES (:grade, :location, :user_id)")
        db.session.execute(sql, {"grade": grade, "location": location, "user_id": user_id})
        db.session.commit()
        return True
    else:
        return False