import base64
from flask import render_template, request, redirect, flash
from app import app

import climbs
import users
import comments
import flashes
import locations
import images

# TODO: index page should show maybe max 20 recent climbs
@app.route("/")
def index():
    routes = climbs.get_all_climbs()
    count = climbs.amount_of_climbs()
    return render_template("index.html", routes=routes, count=count)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/new")
def new():
    grades = climbs.valid_grades()
    all_locations = locations.get_all_locations()
    return render_template("new.html", locations=all_locations, grades=grades)

@app.route("/create", methods=["POST"])
def create():
    grade, location, indoor = request.form["grade"], request.form["locations"], request.form["indoor"]
    flashed = True if "flash" in request.form else False
    content = {"grade": grade, "location": location, "indoor": indoor, "flash": flashed}
    if not climbs.check_climb_content(content=content):
        flash("Invalid inputs. Location must be at least 3 letter.", category="error")
        return redirect("/new")

    new_climb = climbs.create_climb(content=content)    # (bool, route_id)

    # TODO: this implementation works, but isn't very pretty
    if new_climb[0]:
        if "img" in request.files:
            image = request.files["img"]
            if image.filename != "":
                if not images.upload_image(image=image, route_id=new_climb[1]):
                    flash("Check your image file format", category="error")
                    return redirect("/new")
        flash("Route added!", category="success")
        return redirect(f"/climb/{new_climb[1]}")
    flash("You have to be logged in to add a route.", category="error")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            flash("You are now logged in", category="success")
            return redirect("/")
        flash("Check your username and password", category="error")
        return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password"]
        password2 = request.form["password2"]
        if password1 != password2:
            flash("Passwords don't match", category="error")
            return redirect("/register")
        if not users.valid_register(username, password1):
            flash("""Invalid username or password. Username must be at least 3 letters
            and password 6 letters.""", category="error")
            return redirect("/register")
        if users.register(username, password1):
            flash("Account created! You're now logged in.", category="success")
            return redirect("/")
        flash("Failed to register. Try a different username.", category="error")
        return redirect("/register")

@app.route("/logout")
def logout():
    users.logout()
    flash("Logged out.", category="success")
    return redirect("/")

@app.route("/climb/<int:id>")
def climb(id):
    route = climbs.get_climb_by_id(id)
    contents = comments.get_comments_by_climb(id)
    image_info = images.get_image(id)
    image = base64.b64encode(image_info.img).decode("ascii") if image_info else None
    return render_template(
        "climb.html", route=route, contents=contents, 
        image_info=image_info, image=image)

@app.route("/comment/<int:id>", methods=["POST"])
def comment(id):
    content = (request.form["content"], id)
    if comments.add_comment(content):
        return redirect(f"/climb/{id}")
    flash("Something went wrong...", category="error")
    return redirect("/")

@app.route("/user/<int:id>")
def user_page(id):
    routes = climbs.get_climbs_by_user(id)
    hardest_route = climbs.get_users_hardest_climb(id)
    user_flashes = list(map(lambda f: f[0], flashes.get_flashes(id)))
    count = climbs.amount_of_climbs(id)
    username = users.get_name_by_id(id)
    user_comments = comments.get_user_comments(id)

    grade_distribution = climbs.get_user_grade_distribution(id)
    labels = [row[0] for row in grade_distribution]
    values = [row[1] for row in grade_distribution]

    return render_template(
        "user.html", routes=routes, count=count, username=username, hardest_route=hardest_route,
        user_comments=user_comments, flashes=user_flashes, labels=labels, values=values)  


@app.route("/delete/<int:id>", methods=["POST"])
def remove_climb(id):
    if climbs.delete_climb(id):
        flash("Climb deleted.", category="success")
        return redirect(f"/user/{users.user_id()}")
    flash("Something went wrong...", category="error")
    return redirect("/")

@app.route("/delete/comment/<int:id>", methods=["POST"])
def remove_comment(id):
    comment_climb = comments.get_comment_climb(id)
    if comments.remove_comment(id):
        flash("Comment deleted.", category="success")
        return redirect(f"/climb/{comment_climb}")
    flash("Something went wrong...", category="error")
    return redirect("/")
