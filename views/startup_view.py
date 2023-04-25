from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity

import models.startup_model as startup_db
import models.auth_model as user_db

startup = Blueprint('startup', __name__, template_folder="templates")


@startup.route('/')
def startup_home():
    # Home page of startups
    startups = startup_db.get_startups()

    return render_template('startups.html', startups=startups)


@startup.route('/feed')
def feed():
    return render_template('feed.html')


@startup.route('/<startupid>')
def startup_info(startupid):
    startup_data = startup_db.get_startup(startupid)
    founder = user_db.get_info(startup_data['founder'])

    return render_template('startup.html', startup=startup_data, founder=founder)


@startup.route('/addblog', methods=['GET', 'POST'])
@jwt_required(locations='cookies')
def add_blog():
    # Create new blog

    user = get_jwt_identity()
    company = startup_db.get_startup(founder=user['sub'])['_id']

    if request.method == 'GET':
        return render_template('create_blog.html', company=company)
    elif request.method == 'POST':
        title = request.form.get('title')
        blog_id = ''.join(title.split())

        blog_data = {
            "_id": blog_id,
            "title": title,
            "date": datetime.today().strftime('%Y-%m-%d'),
            "content": request.form.get('content'),
            "company": company
        }

        startup_db.add_blog(blog_data)
        return redirect(url_for('startup.blog', blogid=blog_id))


@startup.route('/blog/<blogid>')
def blog(blogid):
    blog_data = startup_db.get_blog(blogid)
    company_data = startup_db.get_startup(name=blog_data['company'])

    return render_template('blog.html', blog=blog_data, company=company_data)

