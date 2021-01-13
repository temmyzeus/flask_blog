from flask_blog.models import User, Post
from flask import render_template, url_for, redirect, flash, request
from flask_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_blog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os

posts = [
    # Dummy Post 1
    {
        "author": "Temiloluwa Awoyele",
        "title": "Blog Post 1",
        "content": """Lorem ipsum dolor sit amet consectetur, 
        adipisicing elit. Earum accusantium quaerat a voluptatem consectetur 
        quod incidunt libero aperiam ducimus, reiciendis magni reprehenderit mollitia
        magnam voluptatum velit at sit laudantium amet!""",
        "date_posted": "Jan 24 2020"
    },
    # Dummy Post 2
    {
        "author": "Ayomide Babalolu",
        "title": "Blog Post 2",
        "content": """Lorem ipsum dolor sit amet consectetur, 
        adipisicing elit. Earum accusantium quaerat a voluptatem consectetur 
        quod incidunt libero aperiam ducimus, reiciendis magni reprehenderit mollitia
        magnam voluptatum velit at sit laudaLoginFormntium amet!""",
        "date_posted": "April 12 2019"
    }
]


# To make flask route to 2 differrnt paths, i.e / & /home
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts, title="Home")


@app.route("/about")
def about():
    return render_template("about.html", title="About", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    # If Current user is authenticated, redirect to homepage
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegistrationForm()
    # To check Validation
    if form.validate_on_submit():
        # Hash user password
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")

        # Collect data form the Form Fields and instantiate to the "User" Model
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)

        # Add User
        db.session.add(user)
        # Create user Account
        db.session.commit()
        flash("Your account has been created you're now able to login!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    # If Current user is authenticated, redirect to homepage
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash(f"Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    # Log User Out
    logout_user()
    return redirect(url_for("home"))


def save_picture(form_picture):
    """Saves picture to server."""
    random_filename = secrets.token_hex(10)
    ext = os.path.splitext(form_picture.filename)[-1]
    filename = random_filename + ext
    file_path = os.path.join(app.root_path, "static/profile_pics", filename)
    form_picture.save(file_path)
    return filename


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form =  UpdateAccountForm()
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    if form.validate_on_submit():
        # Check if there is any picture data since this isn't a required field
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account Updated!!!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", current_user=current_user, image_file=image_file, title="Account", form=form)


@app.route("/<any>")
def not_found(any):
    """Return the not_found.html file when non-exisiting path is entered"""
    return render_template("not_found.html", path=any)
