from app import app
import climbs
import users
from flask import render_template, request, redirect

@app.route("/")
def index():
    routes = climbs.get_all_climbs()
    return render_template("index.html", routes=routes)

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