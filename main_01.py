from flask import Flask, redirect, render_template
from flask_login import LoginManager, login_required, login_user, logout_user

from data import db_session
from data.users import User
from data.jobs import Job
from forms.login import LoginForm
from forms.jobs import JobForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/database.db")


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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/job_add', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Job()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление работы', form=form)


def main():
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
