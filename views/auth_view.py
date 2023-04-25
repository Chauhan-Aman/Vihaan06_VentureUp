from flask import Blueprint, render_template, request, make_response, redirect, session, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


import models.auth_model as user_db
import models.startup_model as startup_db
import tools.image as image

auth = Blueprint("auth", __name__, template_folder="templates")


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_data = user_db.get_info(username)

        if user_data:
            # authenticate user
            if password == user_data['pass']:
                # authentication successful

                payload = {
                    "sub": username,
                    "role": user_data['role']
                }

                access_token = create_access_token(identity=payload)
                resp = make_response(redirect('/'))
                resp.set_cookie('access_token_cookie', access_token)

                print(f"{username} successfully logged-in")
                return resp
        print(f"{username} failed to login, password: {password}")
        return render_template('login.html')


@auth.route('/logout')
@jwt_required(locations='cookies')
def logout():
    user = get_jwt_identity()

    resp = make_response(redirect('/'))
    resp.set_cookie('access_token_cookie', '', expires=0)

    print(f"{user['sub']} has successfully logged out!")
    return resp


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        role = request.form.get('role')

        data = {
            "_id": username,
            "name": name,
            "pass": password,
            "email": email,
            "role": role,
            "registration": False
        }
        
        user_db.register(data)
        print(f"New account created: {username}")

        payload = {
            "sub": username,
            "role": role
        }

        access_token = create_access_token(identity=payload)
        resp = make_response(redirect('/'))
        resp.set_cookie('access_token_cookie', access_token)

        return resp


@auth.route('/register', methods=['GET', 'POST'])
@jwt_required(locations='cookies')
def register():
    user = get_jwt_identity()

    user_data = user_db.get_info(user['sub'])
    if user_data['registration']:
        # user have already registered
        return redirect('/')
    
    if request.method == 'GET':
        # check user's role and display form if GET
        if user['role'] == 'startup':
            return render_template('startup_form.html', user=user_data)
        elif user['role'] == 'mentor':
            return render_template('mentor_form.html', user=user_data)
        elif user['role'] == 'investor':
            return render_template('investor_form.html', user=user_data)
    elif request.method == 'POST':
        if user['role'] == 'startup':
            company_logo = request.files['logo']
            founder_pfp = request.files['founder_pfp']
            name = request.form.get('name')
 
            startup_data = {
                "_id": ''.join(name.split()),
                "name": request.form.get('name'),
                "logo": image.upload(company_logo, ''.join(name.split()), 'Startups')['secure_url'],
                "short_description": request.form.get('short_description'),
                "long_description": request.form.get('long_description'),
                "domain": request.form.get('domain'),
                "url": request.form.get('url'),
                "founded_year": request.form.get('founded_year'),
                "team_size": request.form.get('team_size'),
                "location": request.form.get('location'),
                "pfp": image.upload(founder_pfp, user['sub'], 'Users')['secure_url'],
                "founder": user['sub'],
                "twitter": request.form.get('twitter'),
                "linkedin": request.form.get('linkedin'),
                "investors": [],
                "mentors": [],
                "requests": []
            }

            startup_db.register_startup(startup_data)

            # TODO: redirect to startup page
            return redirect('/')
        elif user['role'] == 'mentor':
            mentor_pfp = request.files['mentor_pfp']
            mentor_data = {
                "domain": request.form.get('domain'),
                "pfp": image.upload(mentor_pfp, user['sub'], 'Users')['secure_url'],
                "twitter": request.form.get('twitter'),
                "linkedin": request.form.get('linkedin'),
                "clients": [],
                "requests": [],
                "posts": [],
                "registration": True
            }

            user_db.register_mentor(user['sub'], mentor_data)

            # TODO: return to mentor profile
            return redirect('/')
        elif user['role'] == 'investor':
            investor_pfp = request.files['investor_pfp']
            investor_data = {
                "domain": request.form.get('domain'),
                "pfp": image.upload(investor_pfp, user['sub'], 'Users')['secure_url'],
                "twitter": request.form.get('twitter'),
                "linkedin": request.form.get('linkedin'),
                "clients": [],
                "requests": []
            }

            user_db.register_investor(user['sub'], investor_data)

            # TODO: return to company page
            return redirect('/')
