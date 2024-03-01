from sqlalchemy.sql import text
from db import db
import users

def get_all_locations():
    sql = "SELECT * FROM locations;"
    result = db.session.execute(text(sql))
    return result.fetchall()
