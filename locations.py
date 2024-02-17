from db import db
from sqlalchemy.sql import text
import users

def get_all_locations():
    sql = text("SELECT * FROM locations;")
    result = db.session.execute(sql)
    return result.fetchall()

def add_location(content):
    if users.is_admin():
        # TODO: 
        pass