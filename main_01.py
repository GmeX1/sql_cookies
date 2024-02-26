from flask import Flask, redirect, render_template
from flask_login import LoginManager, login_user
import sys

sys.path.append('..')

from data import db_session
from data.users import User
from forms.login import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/database.db")
# session = db_session.create_session()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


def main():
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()

    # user = User()
    # user.surname = "Scott"
    # user.name = "Ridley"
    # user.age = 21
    # user.position = "captain"
    # user.speciality = "research engineer"
    # user.address = "module_1"
    # user.email = "scott_chief@mars.org"
    # user.hashed_password = "cap"
    # session.add(user)
    # session.commit()
