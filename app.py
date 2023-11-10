"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
# from flask_debugtoolbar import DebugToolbarExtension
# Commented this line out because it's causing an error
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'itsasecret'

# toolbar = DebugToolbarExtension(app)
# Commented this line out because it's causing an error

connect_db(app)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()


@app.route('/')
def home():
    """Homepage: 
    Shows a list of posts & sorted by most recent post first.
    """

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)

    # return redirect('/users')


@app.errorhandler(404)
def page_not_found(evt):
    """Shows error 404 (NOT FOUND)."""

    return render_template('404.html'), 404


# --- Routes for Users ---


@app.route('/users')
def users_index():
    """Page that shows users' info"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Page for a form to create a new user"""

    return render_template('users/new.html')


@app.route("/users/new", methods=["POST"])
def users_new():
    """Page to create a new user based on the form submission."""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    flash(f"New User: {new_user.first_name} {new_user.last_name} added!")
    return redirect("/users")


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Page that shows user details for a specific user."""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Page that shows a form to edit an existing user's information."""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Page to update an existing user's information based on the form submission."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Page to delete an existing user based on form submission."""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    flash(f"User '{user.first_name} {user.last_name}' has been delted! ")
    return redirect("/users")


# --- Routes for posts ---


@app.route('/users/<int:user_id>/posts/new')
def posts_new_content(user_id):
    """Shows where to enter a new post for a specific user."""

    user = User.query.get_or_404(user_id)

    return render_template('posts/new.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def posts_new(user_id):
    """Process the form submission to create a new post for a specific user."""

    user = User.query.get_or_404(user_id)
    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user_id=user.id  # Pass the user object
    )

    db.session.add(new_post)
    db.session.commit()

    flash(f"New post '{new_post.title}' added!")
    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page for a specific post."""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Provides a form to allow the user to edit a post."""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handles the submitted form to update an existing post."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    flash(f"Post '{post.title}' has been editted!")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_delete(post_id):
    """Handles deleting an existing post."""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash(f"Post '{post.title}' has been deleted!")

    return redirect(f"/users/{post.user_id}")
