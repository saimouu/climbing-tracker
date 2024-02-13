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
    flash = request.form["flash"]
    if request.form["indoor"] == "indoor":
        indoor = True
    else:
        indoor = False

    if climbs.create_climb({"grade": grade, "location": location, "indoor": indoor, "flash": flash}):
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
        if not users.valid_register(username, password1):
            return render_template("error.html", message="invalid username or password. username must be atleast 4 letters and password 6.")
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
    hardest_route = climbs.get_users_hardest_climb(id)
    username = users.get_name_by_id(id)
    # fix: user sql count not len
    return render_template("user.html", routes=routes, count=len(routes), username=username, hardest_route=hardest_route)  

# fix redirect
@app.route("/delete/<int:id>")
def remove_climb(id):
    if climbs.delete_climb(id):
        return redirect("/")
    return redirect("error.html", message="something went wrong...")