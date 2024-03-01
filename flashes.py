from sqlalchemy.sql import text
from db import db

def add_flash_data(route_id, user_id, flash):
    sql = """
        INSERT INTO flashes (route_id, user_id, flash) 
        VALUES (:route_id, :user_id, :flash);
    """
    db.session.execute(text(sql), {"route_id": route_id, "user_id": user_id, "flash": flash})
    db.session.commit()

def get_flashes(user_id):
    sql = """
        SELECT route_id FROM flashes 
        WHERE user_id=:user_id AND flash=TRUE;
    """
    result = db.session.execute(text(sql), {"user_id": user_id}).fetchall()
    return result

def user_avg_flash(user_id):
    sql = """
        SELECT ROUND(AVG(F.flash::INT) * 100, 1) 
        FROM Flashes F 
        LEFT JOIN Routes R ON F.route_id=R.id AND F.user_id=R.user_id 
        WHERE F.user_id=:user_id AND R.visible=TRUE;
    """
    result = db.session.execute(text(sql), {"user_id": user_id}).fetchone()
    return result[0]
