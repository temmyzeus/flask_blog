from flask import Flask, render_template, url_for, redirect, flash
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

#Set Secret Key
app.config["SECRET_KEY"] = '3854bf36bf4e17cf1e8f8b778a0bc343'

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
    form = RegistrationForm()
    #To check Validation
    if form.validate_on_submit():
        flash(f"Account Created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Login successful for user {form.email.data}", "success")
        return redirect(url_for("home"))
    return render_template("login.html", title="Login" ,form=form)

  
if __name__ == "__main__":
    app.run(debug=True)
