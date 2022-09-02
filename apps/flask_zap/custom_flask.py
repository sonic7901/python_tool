from flask import (
    Flask,
    send_from_directory,
    redirect,
    render_template,
    request,
    jsonify
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
from werkzeug.utils import secure_filename
import time
import db.custom_sqlite as sql_db
import models.scan
import shutil


# config init
config = configparser.ConfigParser()
config.read("config.ini")

# flask init
flask_app = Flask(__name__)
flask_app.secret_key = config.get("flask", "secret_key")
flask_app.config['UPLOAD_FOLDER'] = config.get("flask", "upload_folder")
allow_extension = {'py', 'jpg'}


users = {}

# Flask-Login init
login_manager = LoginManager()
login_manager.init_app(flask_app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message = "not work"


# 1. login module

class User(UserMixin):
    pass


def update_user():
    list_user = sql_db.read_data_users('db/test.db')
    for temp_user in list_user:
        users[temp_user[0]] = {'password': temp_user[1]}


@flask_app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/index")

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
        return redirect("/index")
    return redirect("/login")


@login_manager.user_loader
def user_loader(user_id):
    if user_id not in users:
        return

    user = User()
    user.id = user_id
    return user


# 2. api

@flask_app.route("/issue")
def issue_test():
    temp_issues = sql_db.read_data_issues('db/test.db')
    print(temp_issues)
    return render_template("custom_issue.html", issue_list=temp_issues)


@flask_app.route("/select", methods=["POST"])
def select_test():
    list_issues = sql_db.read_data_issues('db/test.db')
    print(str(request.form["issue_id"]))
    single_issue = sql_db.read_issue_by_id('db/test.db', request.form["issue_id"])
    list_select = []
    for issue in list_issues:
        temp_issue = list(issue)
        if str(temp_issue[0]) == str(request.form["issue_id"]):
            temp_issue.append("selected")
            list_select.append(temp_issue)
        else:
            temp_issue.append(" ")
            list_select.append(temp_issue)
    return render_template("custom_issue.html",
                           issue_list=list_select,
                           input_score=single_issue[0],
                           input_weight=single_issue[1],
                           input_name_zh=single_issue[2],
                           input_name_en=single_issue[3],
                           input_desc_zh=single_issue[4],
                           input_desc_en=single_issue[5],
                           input_solu_zh=single_issue[6],
                           input_solu_en=single_issue[7])


@flask_app.route("/index", methods=["GET"])
@login_required
def index():
    temp_fields = ['COMPANY', 'URL', 'STATUS', 'Report']
    temp_column = sql_db.read_data_missions('db/test.db')
    temp_issues = sql_db.read_data_issues('db/test.db')
    list_column = []
    for single_column in temp_column:
        test_column = list(single_column)
        if test_column[3] == '':
            test_column.append("disabled")
        else:
            test_column.append("")
        list_column.append(test_column)
    return render_template("custom_index.html",
                           labels=temp_fields,
                           column_testcase=list_column,
                           issue_list=temp_issues)


@flask_app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(flask_app.root_path, "static"),
                               "favicon.ico",
                               mimetype="image/vnd.microsoft.icon")


@flask_app.route("/report/<temp_path>/<temp_file>", methods=["GET"])
@login_required
def result_file(temp_path, temp_file):
    print(flask_app.root_path + "\\report\\")
    return send_from_directory(os.path.join(flask_app.root_path + "\\report\\", temp_path), temp_file)


@flask_app.route('/upload', methods=['POST'])
@login_required
def uploaded_file():
    import utils.custom_file
    file = request.files['file']
    temp_name = request.form['mission_company']
    temp_url = request.form['mission_url']
    temp_target = request.form['mission_target']
    if file:
        filename = secure_filename(file.filename)
        print(flask_app.config['UPLOAD_FOLDER'])
        if os.path.isdir(flask_app.config['UPLOAD_FOLDER']):
            file.save(os.path.join(flask_app.config['UPLOAD_FOLDER'], filename))
            print("upload success")
            filename_only = utils.custom_file.read_name(filename)
        else:
            sql_db.add_mission('db/test.db', temp_url, temp_name, temp_target)
            print("folder not exist, please check config")
    else:
        sql_db.add_mission('db/test.db', temp_url, temp_name, temp_target)
        print("folder not exist, please check config")
    return redirect("/index")


# 3. error handle
@flask_app.errorhandler(404)
def page_not_found(e):
    return redirect("/index")


def check_response(temp_html, temp_str):
    check_status = False
    if temp_str == '':
        check_status = True
    if temp_str in temp_html:
        check_status = True
    return check_status


def allowed_file(filename):
    if filename.rsplit('.', 1)[1].lower() in allow_extension:
        print('t2')
    if '.' in filename:
        print('t3')
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allow_extension


def unit_test_report():
    import pathlib
    # file path
    template_path = str(pathlib.Path(__file__).parent.absolute()) + "\\"
    shutil.copyfile(template_path + '\\models\\example.json', template_path + '\\models\\temp.json')
    models.scan.run_check()


# 3. main
def create_app():
    # unit_test_report()
    models.scan.scan_thread()
    update_user()
    flask_app.debug = True
    flask_app.run(host="0.0.0.0", port=8123, debug=False)
