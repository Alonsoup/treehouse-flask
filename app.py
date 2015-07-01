from flask import Flask, g, render_template, flash, redirect, url_for
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import LoginManager, login_user, logout_user, login_required

import forms
import models

DEBUG=True
PORT=8000
HOST='0.0.0.0'

app = Flask(__name__)
app.secret_key = 'AAAAB3NzaC1yc2EAAAADAQABAAACAQDLvZb03Z5OmmcC+8pPexv1E4++TVkpg8fQYFsg/iJsYzkw9+SBWTtKtZW+yb7M19Oy6YwEWiMZsWVn8P6Bx+E957Arb/uS7PCt5UUQgqLpRlxkTvVJgEouCA7ciMvygcHJno5f9JJwAbM5hHm0edgdK43Dksfy82lpIEsEmLoNBlxHEcg5TBdZ75634cydoJ5drKdA+xxXyfNZyweEHdOCbACkcJ5TGsbRkSsIHDhCLkns17a8oJVPfNJOhX0dF/6DQIzEnyyFzn/VWXTnNCXBZ46jYD7QSDiDAWsoVjDrJyeL/PYFIUoEyXmQViyNywYzsb+B2Di5OIvA1oW602j076jWzkIsgnoLGrpYZx5cwcCl6DohkAoH+tg7zaBR61WEOmb8LXNs8Kc5lozP8rXHh+BpFoBi4R7fV8G+vtRK3Yrebhnv7zHKFO0CBLgOP1w+BFkCnh/mq/xKlmKMSscjZSYSoO15QKEeFd/EnnbEV6V1AC7wnFv6gRffoQdBOpTUBVZhHK3LPSVzCOu/D5Hxz4m2FLKmuhWtwMSX8p2JiILVgkZScOSNcTpi2Rs8dF1IahJKTwuo87v68AkqgeheCink773g6fGDmaaheKvddjYVQLJ5g7bGuBdL+mGiowKhrwHNuJVGgBDpt/HiDKqjKfcB/4ZQ9hYwEFTyhebY2'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None




@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you registered!", "success")
        models.User.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))



@app.route('/')
def index():
    return render_template("index.html")



if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='admin',
            email='braden@treehouse.com',
            password='password',
            admin=True
        )
    except ValueError:
        pass

    app.run(debug=DEBUG, host=HOST, port=PORT)















