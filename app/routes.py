from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Property
from . import db

routes = Blueprint("routes", __name__)


@routes.route("/")
def home():
    return redirect("/properties")


# ---------------- АВТОРИЗАЦИЯ ----------------

@routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        user = User(username=username, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect("/properties")

        return "Неверный логин или пароль"

    return render_template("login.html")


@routes.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------- НЕДВИЖИМОСТЬ ----------------

@routes.route("/properties")
def properties():
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")

    query = Property.query

    if min_price:
        query = query.filter(Property.price >= min_price)

    if max_price:
        query = query.filter(Property.price <= max_price)

    properties = query.all()

    return render_template("properties.html", properties=properties)


@routes.route("/add_property", methods=["GET", "POST"])
def add_property():
    if request.method == "POST":
        new_property = Property(
            title=request.form["title"],
            type=request.form["type"],
            price=request.form["price"],
            area=request.form["area"],
        )

        db.session.add(new_property)
        db.session.commit()

        return redirect("/properties")

    return render_template("add_property.html")


@routes.route("/edit_property/<int:id>", methods=["GET", "POST"])
def edit_property(id):
    property = Property.query.get(id)

    if request.method == "POST":
        property.title = request.form["title"]
        property.type = request.form["type"]
        property.price = request.form["price"]
        property.area = request.form["area"]

        db.session.commit()

        return redirect("/properties")

    return render_template("edit_property.html", property=property)


@routes.route("/delete_property/<int:id>")
def delete_property(id):
    property = Property.query.get(id)

    db.session.delete(property)
    db.session.commit()

    return redirect("/properties")