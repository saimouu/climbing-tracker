from db import db
from sqlalchemy.sql import text

def add_flash_data(route_id, user_id, flash):
    try:
        sql = text("INSERT INTO flashes (route_id, user_id, flash) VALUES (:route_id, :user_id, :flash);")
        db.session.execute(sql, {"route_id": route_id, "user_id": user_id, "flash": flash})
        db.session.commit()
        return True
    except:
        return False

def get_flashes(user_id):
    sql = text("SELECT route_id FROM flashes WHERE user_id=:user_id AND flash=TRUE;")
    result = db.session.execute(sql, {"user_id": user_id}).fetchall()
    return result
