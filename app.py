from datetime import timedelta

from flask import Flask, redirect, render_template, session, url_for
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required

from views.auth_view import auth
from views.startup_view import startup

import config.secrets as secrets

app = Flask(__name__)
app.secret_key = secrets.APP_SECRET
app.config['JWT_SECRET_KEY'] = secrets.JWT_SECRET
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=4)


jwt = JWTManager(app)


@jwt.unauthorized_loader
def custom_unauthorized_response(_err):
    return redirect(url_for('auth.login'))


@jwt.expired_token_loader
def custom_expired_token_response(jwt_header, jwt_payload):
    return redirect(url_for('auth.login'))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/profile')
@jwt_required(locations='cookies')
def profile():
    user = get_jwt_identity()
    return "PROFILE"


# Register blueprint
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(startup, url_prefix='/startup')


if __name__ == "__main__":
    app.run(debug=True)
