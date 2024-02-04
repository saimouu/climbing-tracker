from app import app
import climbs, users, comments
from flask import render_template, request, redirect

# fix naming because now routes = climbs, it's confusing

@app.route("/")
def index():
    if users.user_id() != 0:
        routes = climbs.get_all_climbs()
        return render_template("index.html", routes=routes, count=len(routes))
    else:
        return redirect("/login")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    grade = request.form["grade"]
    location = request.form["location"]
    if climbs.create_climb((grade, location)):
        return redirect("/")
    else:
        return render_template("error.html", message="you are not logged in")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="wrong username or password")
        
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="password don't match")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="failed to register, try different username")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/climb/<int:id>")
def climb(id):
    route = climbs.get_climb_by_id(id)
    contents = comments.get_comments_by_climb(id)
    return render_template("climb.html", route=route, contents=contents)

@app.route("/comment/<int:id>", methods=["POST"])
def comment(id):
    content = (request.form["content"], id)
    if comments.add_comment(content):
        return redirect(f"/climb/{id}")

@app.route("/user/<int:id>")
def user_page(id):
    routes = climbs.get_climbs_by_user(id)
    username = users.get_name_by_id(id)
    return render_template("user.html", routes=routes, count=len(routes), username=username)

@app.route("/delete/<int:id>")
def remove_climb(id):
    if climbs.delete_climb(id):
        return redirect("/")
    return redirect("error.html", message="something went wrong...")