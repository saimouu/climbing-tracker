from sqlalchemy.sql import text
from db import db

def add_flash_data(route_id, user_id, flash):
    try:
        sql = """
            INSERT INTO flashes (route_id, user_id, flash) 
            VALUES (:route_id, :user_id, :flash);
        """
        db.session.execute(text(sql), {"route_id": route_id, "user_id": user_id, "flash": flash})
        db.session.commit()
        return True
    except:
        return False

def get_flashes(user_id):
    sql = """
        SELECT route_id FROM flashes 
        WHERE user_id=:user_id AND flash=TRUE;
    """
    result = db.session.execute(text(sql), {"user_id": user_id}).fetchall()
    return result
