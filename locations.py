from sqlalchemy.sql import text
from db import db
import users

def get_all_locations():
    sql = "SELECT * FROM locations;"
    result = db.session.execute(text(sql))
    return result.fetchall()

def add_location(content):
    if users.is_admin():
        # TODO:
        pass
