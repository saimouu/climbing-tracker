from db import db
from sqlalchemy.sql import text
from werkzeug.utils import secure_filename

# Flask docs: Uploading Files
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(image, route_id):
    if allowed_file(image.filename):
        filename = secure_filename(image.filename)
        mimetype = image.mimetype
        img = image.read()

        sql = text("INSERT INTO images (img, name, mimetype, route_id) VALUES (:img, :name, :mimetype, :route_id)")
        db.session.execute(sql, {"img": img, "name": filename, "mimetype": mimetype, "route_id": route_id})
        db.session.commit()
        return True
    return False

def get_image(route_id):
    sql = text("SELECT * FROM images WHERE route_id=:route_id")
    result = db.session.execute(sql, {"route_id":route_id}).fetchone()
    return result