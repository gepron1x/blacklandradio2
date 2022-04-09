from flask import Flask, render_template
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from data import db_session
from register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blacklandradio.db")
    app.run()


@app.route("/index")
def index():
    return render_template("base.html", title="Blackland Radio")


@app.route("/register", methods=['GET', 'POST'])
def register():
    from data.user import BlacklandUser
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(BlacklandUser).filter(BlacklandUser.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = BlacklandUser(
            login=form.login.data,
            password=generate_password_hash(form.password.data),
            description=form.description.data
        )
        db_sess.add(user)
        db_sess.commit()
        return redirect('/index')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
