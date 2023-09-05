from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from db import db
from models import PostModel

main = Blueprint("main", __name__, static_folder="static",template_folder="templates" )

# Define the index route
@main.route("/")
def index():
    return render_template("index.html")

# Define the profile route
@main.route('/profile')
@login_required
def profile():
    posts = PostModel.query.all()  # Query all posts
    return render_template("profile.html", name=current_user.name, posts=posts)

@main.route('/addNote', methods=['POST'])
def signup_post():
    inputTitle = request.form.get('inputTitle')
    inputPost = request.form.get('inputPost')
  
    new_Post = PostModel(inputTitle=inputTitle, inputPost=inputPost)

    # add the new user to the database
    db.session.add(new_Post)
    db.session.commit()

    return redirect(url_for('main.profile'))

@main.route('/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    post = PostModel.query.get_or_404(post_id)

    # Delete the post from the database
    db.session.delete(post)
    db.session.commit()

    flash('Post deleted successfully', 'success')
    return redirect(url_for('main.profile'))

@main.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = PostModel.query.get_or_404(post_id)

    if request.method == 'POST':
        # Update the post with the new data
        post.inputTitle = request.form.get('inputTitle')
        post.inputPost = request.form.get('inputPost')

        # Commit changes to the database
        db.session.commit()

        flash('Post updated successfully', 'success')
        return redirect(url_for('main.profile'))

    return render_template('edit_post.html', post=post)