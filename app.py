from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, LoginManager
from flask_migrate import Migrate
import food_api
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from forms import RegistrationForm, LoginForm, SearchFood
from models import User


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = SearchFood()
    if form.validate_on_submit():
        print(form.food.data)
        return redirect(url_for('search', q=form.food.data))
    return render_template('index.html', title='Accueil', form=form)


@app.route("/search")
def search():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('search_results.html', food=food_api.search(request.args.get('q')))


if __name__ == '__main__':
    app.run()
