from flask import Blueprint, render_template, request, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity

import models.startup_model as startup_db

mentor = Blueprint('mentor', __name__, template_folder="templates")


@mentor.route('/')
def startup_home():
    # Home page of mentors
    return "Mentors Home"



@mentor.route('/addpost', methods=['GET', 'POST'])
@jwt_required(locations='cookies')
def add_blog():
    # Create new post

    user = get_jwt_identity()

    if user['role'] != 'mentor':
        return redirect('/')

    if request.method == 'GET':
        return render_template('add_blog.html', user=user)
    elif request.method == 'POST':
        title = request.form.get('title')

        post_data = {
            "_id": ''.join(title.split()),
            "title": title,
            "content": request.form.get('content'),
            "creator": user['sub']
        }

        if request.form.get('private') == 'yes':
            post_data['private'] = True
        else:
            post_data['private'] = False

        startup_db.add_blog(post_data)
