from flask import (
    Flask,
    send_from_directory,
    redirect,
    render_template,
    request
)

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    current_user,
)

import configparser
import os
import app.models.api_shell as api_shell
import app.models.custom_shell

# config init
config = configparser.ConfigParser()
config.read("config.ini")

# flask init
app = Flask(__name__)
app.secret_key = config.get("flask", "secret_key")
app.config['UPLOAD_FOLDER'] = './src/upload'
allow_extension = {'py'}

# users list
users = {"onedegree": {"password": "onedegree9527"}}

# Flask-Login init
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message = "not work"


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(user_id):
    if user_id not in users:
        return

    user = User()
    user.id = user_id
    return user


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return render_template("custom_main.html")

    if request.method == "GET":
        return render_template("custom_login.html")

    user_id = request.form["user_id"]
    user_id = str(user_id)
    if len(user_id) > 64 or len(user_id) == 0:
        return redirect("/login")
    elif (user_id in users) and (request.form["password"] == users[user_id]["password"]):
        user = User()
        user.id = user_id
        login_user(user)
        return render_template("custom_main.html")
    return redirect("/login")


@app.route("/index", methods=["GET"])
@login_required
def index():
    return render_template("custom_main.html")


@app.route("/demo", methods=["GET", "POST"])
@login_required
def demo():
    return render_template("custom_demo.html")


@app.route("/shell", methods=["GET"])
@login_required
def shell():
    with open('temp/test.txt', 'a') as temp_file:
        temp_lines = ['']
        try:
            temp_lines = temp_file.readlines()
        except Exception as ex:
            print('Exception:' + str(ex))

    return render_template("custom_shell.html", result_list=temp_lines)


@app.route("/shell", methods=["POST"])
@login_required
def shell_post():
    print(request.form['html_input'])
    # app.models.api_shell.run()
    api_shell.run(request.form['html_input'], 'temp/test.txt')
    temp_lines = []
    with open('temp/test.txt') as temp_file:
        temp_lines = temp_file.readlines()
    return render_template("custom_shell.html", result_list=temp_lines)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"),
                               "favicon.ico",
                               mimetype="image/vnd.microsoft.icon")


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/index")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allow_extension


def create_app():
    app.debug = True
    app.run(host="0.0.0.0", port=8123)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8123)
