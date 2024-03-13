from datetime import datetime

from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from forms.user import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    user = User()
    user.name = "Ridley"
    user.about = "Scott"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    db_sess = session.create_session()
    db_sess.add(user)
    job = Jobs()
    job.team_leader = 1
    job.job = "deployment of residential modules 1 and 2"
    job.age = 21
    job.work_size = 15
    job.collaborators = "2, 3"
    job.start_date = datetime.now()
    job.is_finished = False
    db_sess = session.create_session()
    db_sess.add(job)
    db_sess.commit()
    #app.run(port=8080, host='127.0.0.1')

@app.route("/")
def index():
    db_sess = db_session.create_session()
    return render_template("index.html", news=None)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login')
def login():
    return "-200"

if __name__ == '__main__':
    main()
