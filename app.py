from flask import Flask, request, redirect, render_template

# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.app_context().push()

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "shhhsecret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.route("/")
def root():
    """Homepage redirects to list of users."""

    return redirect("/users")


@app.route("/users")
def users_index():
    """Page with Users information"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users/index.html", users=users)


@app.route("/users/new", methods=["GET"])
def users_new_form():
    """Show new user form"""

    return render_template("users/new.html")


@app.route("/users/new", methods=["POST"])
def users_new():
    """Handles submission of the new user form"""

    new_user = User(
        first_name=request.form["first_name"],
        last_name=request.form["last_name"],
        image_url=request.form["image_url"] or None,
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def users_show(user_id):
    """Page to show a specific users information"""

    user = User.query.get_or_404(user_id)
    return render_template("users/show.html", user=user)


@app.route("/users/<int:user_id>/edit")
def users_edit(user_id):
    """Exsisting user edit form"""

    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def users_update(user_id):
    """handles submission of a user editing their information"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def users_destroy(user_id):
    """Handles submission for deleting a user and their information"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
