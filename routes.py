from app import app
import climbs, users, comments
from flask import render_template, request, redirect

@app.route("/")
def index():
    if users.user_id() != 0:
        routes = climbs.get_all_climbs()
        return render_template("index.html", routes=routes)
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
        password = request.form["password"]
        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="failed to register")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/climb/<int:id>")
def climb(id):
    route = climbs.get_climb_by_id(id)
    contents = comments.get_comments_by_climb(id)
    print(contents)
    return render_template("climb.html", route=route, contents=contents)    # fix naming....

@app.route("/comment/<int:id>", methods=["POST"])
def comment(id):
    content = (request.form["content"], id)
    if comments.add_comment(content):
        return redirect(f"/climb/{id}")