from flask import Flask, render_template, request, make_response
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


def main():
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    login_manager = LoginManager()
    login_manager.init_app(app)
    # db_session.global_init("db/mars_explorer.db")
    # session = db_session.create_session()
    main()
