from flask import (
    Flask,
    send_from_directory,
    redirect,
    url_for,
    render_template,
    request,
    flash,
    jsonify,
)
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)

# from apscheduler.schedulers.blocking import BlockingScheduler
import configparser
# import read_report
import subprocess
import os
import json
import csv
import sys
import threading
import random
import time
import signal
import datetime

import custom_shell

# config init
config = configparser.ConfigParser()
config.read("config.ini")

# flask init
app = Flask(__name__)
app.secret_key = config.get("flask", "secret_key")

# users list
users = {"onedegree": {"password": "onedegree9527"}}

# Flask-Login init
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message = "not work"

# scheduled init
# schedule = BlockingScheduler()


def signal_handler(signal, frame):
    print("exiting")
    sys.exit(0)


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
    elif (user_id in users) and (
        request.form["password"] == users[user_id]["password"]
    ):
        user = User()
        user.id = user_id
        login_user(user)
        return render_template("custom_main.html")
    return redirect("/login")


def read_date(request_temp, data_type):
    try:
        request_data = request_temp.data
        request_enc = str(request_data, encoding="utf-8")
        request_data_json = json.loads(request_enc)
        result = request_data_json[data_type]
    except Exception as ex:
        # logging.warning('read_date error')
        print(str(ex) + "\n")
        result = ""
    return result


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
    return render_template("custom_shell.html")


@app.route("/shell", methods=["POST"])
@login_required
def shell_post():
    temp_input = request.form['html_input']
    temp_result_list = custom_shell.run_shell(temp_input)
    return render_template("custom_shell.html", result_list=temp_result_list)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, ""),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return redirect("/index")
    # return render_template("custom_main.html")


if __name__ == "__main__":
    # signal.signal(signal.SIGINT, signal_handler)
    # start_runner()
    app.debug = True
    app.run(host="127.0.0.1", port=8123)
