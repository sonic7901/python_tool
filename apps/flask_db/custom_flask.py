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
import db.custom_sqlite as sql_db

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
@flask_app.route("/issue_add")
def issue_add():
    return render_template("custom_issue_add.html")


@flask_app.route("/button_add", methods=["POST"])
def button_add():
    sql_db.add_issue('db/test.db',
                     request.form['origin_name'],
                     request.form['issue_score'],
                     request.form['issue_weight'],
                     request.form['issue_cost'],
                     request.form['name_en'],
                     request.form['name_zh'],
                     request.form['desc_en'],
                     request.form['desc_zh'],
                     request.form['solu_en'],
                     request.form['solu_zh'])
    return redirect("/index")


@flask_app.route("/issue_edit")
def issue_edit():
    temp_issues = sql_db.read_data_issues('db/test.db')
    return render_template("custom_issue_edit.html", issue_list=temp_issues)


@flask_app.route("/issue_type")
def issue_type():
    temp_issues = sql_db.read_data_issues('db/test.db')
    return render_template("custom_issue_type.html", issue_list=temp_issues, temp_label="請由上往下依序選擇")


@flask_app.route("/type_add")
def type_add():
    temp_types = sql_db.read_data('db/test.db', 'TYPE')
    return render_template("custom_type_add.html", type_list=temp_types)


@flask_app.route("/button_edit", methods=["POST"])
def button_edit():
    print("hide_id:" + str(request.form['hide_id']))
    if str(request.form['hide_id']) == '':
        temp_issues = sql_db.read_data_issues('db/test.db')
        return render_template("custom_issue_edit.html", issue_list=temp_issues, temp_label="請先選擇要修改的 issue")
    else:
        sql_db.update_issue('db/test.db',
                            request.form['origin_name'],
                            request.form['issue_score'],
                            request.form['issue_weight'],
                            request.form['issue_cost'],
                            request.form['name_en'],
                            request.form['name_zh'],
                            request.form['desc_en'],
                            request.form['desc_zh'],
                            request.form['solu_en'],
                            request.form['solu_zh'],
                            request.form['hide_id'])

    list_issues = sql_db.read_data_issues('db/test.db')
    single_issue = sql_db.read_issue_by_id('db/test.db', request.form["hide_id"])
    list_select = []
    for issue in list_issues:
        temp_issue = list(issue)
        if str(temp_issue[0]) == str(request.form["hide_id"]):
            temp_issue.append("selected")
            list_select.append(temp_issue)
        else:
            temp_issue.append(" ")
            list_select.append(temp_issue)
    return render_template("custom_issue_edit.html",
                           issue_list=list_select,
                           input_origin=single_issue[0],
                           input_score=single_issue[1],
                           input_weight=single_issue[2],
                           input_cost=single_issue[3],
                           input_name_zh=single_issue[4],
                           input_name_en=single_issue[5],
                           input_desc_zh=single_issue[6],
                           input_desc_en=single_issue[7],
                           input_solu_zh=single_issue[8],
                           input_solu_en=single_issue[9],
                           input_id=request.form["hide_id"])


@flask_app.route("/issue_remove")
def issue_remove():
    temp_issues = sql_db.read_data_issues('db/test.db')
    return render_template("custom_issue_remove.html", issue_list=temp_issues)


@flask_app.route("/button_remove", methods=["POST"])
def button_remove():
    sql_db.delete_issue('db/test.db', request.form["issue_id"])
    # sql_db.delete_tag_by_issue('db/test.db', request.form["issue_id"])
    return redirect("/index")


@flask_app.route("/tag_add")
def tag_add():
    temp_issues = sql_db.read_data_issues('db/test.db')
    return render_template("custom_tag_add.html", issue_list=temp_issues)


@flask_app.route("/button_tag_add", methods=["POST"])
def button_tag_add():
    sql_db.add_tag('db/test.db', request.form['hide_id'], request.form['tag_name'])
    list_issues = sql_db.read_data_issues('db/test.db')
    list_tag = sql_db.read_tag_by_id('db/test.db', request.form["hide_id"])
    list_select = []
    for issue in list_issues:
        temp_issue = list(issue)
        if str(temp_issue[0]) == str(request.form["hide_id"]):
            temp_issue.append("selected")
            list_select.append(temp_issue)
        else:
            temp_issue.append(" ")
            list_select.append(temp_issue)

    return render_template("custom_tag_add.html",
                           issue_list=list_select,
                           tag_list=list_tag,
                           input_id=request.form["hide_id"])


@flask_app.route("/tag_remove")
def tag_remove():
    temp_issues = sql_db.read_data_issues('db/test.db')
    return render_template("custom_tag_remove.html", issue_list=temp_issues)


@flask_app.route("/reference_add")
def reference_add():
    temp_issues = sql_db.read_data_issues('db/test.db')
    return render_template("custom_reference_add.html", issue_list=temp_issues)


@flask_app.route("/button_reference_add", methods=["POST"])
def button_reference_add():
    sql_db.add_reference('db/test.db', request.form['hide_id'],
                         request.form['reference_name'],
                         request.form['reference_value'])
    list_issues = sql_db.read_data_issues('db/test.db')
    list_reference = sql_db.read_reference_by_id('db/test.db', request.form["hide_id"])
    list_select = []
    for issue in list_issues:
        temp_issue = list(issue)
        if str(temp_issue[0]) == str(request.form["hide_id"]):
            temp_issue.append("selected")
            list_select.append(temp_issue)
        else:
            temp_issue.append(" ")
            list_select.append(temp_issue)

    return render_template("custom_reference_add.html",
                           issue_list=list_select,
                           reference_list=list_reference,
                           input_id=request.form["hide_id"])


@flask_app.route("/reference_remove")
def reference_remove():
    temp_issues = sql_db.read_data_issues('db/test.db')
    return render_template("custom_reference_remove.html", issue_list=temp_issues)


@flask_app.route("/button_tag_remove", methods=["POST"])
def button_tag_remove():
    sql_db.delete_tag('db/test.db', request.form["tag_id"])
    list_issues = sql_db.read_data_issues('db/test.db')
    list_tag = sql_db.read_tag_by_id('db/test.db', request.form["hide_id"])
    list_select = []
    for issue in list_issues:
        temp_issue = list(issue)
        if str(temp_issue[0]) == str(request.form["hide_id"]):
            temp_issue.append("selected")
            list_select.append(temp_issue)
        else:
            temp_issue.append(" ")
            list_select.append(temp_issue)

    return render_template("custom_tag_remove.html",
                           issue_list=list_select,
                           tag_list=list_tag,
                           input_id=request.form["hide_id"])


@flask_app.route("/button_reference_remove", methods=["POST"])
def button_reference_remove():
    sql_db.delete_reference('db/test.db', request.form["reference_id"])
    list_issues = sql_db.read_data_issues('db/test.db')
    list_reference = sql_db.read_reference_by_id('db/test.db', request.form["hide_id"])
    list_select = []
    for issue in list_issues:
        temp_issue = list(issue)
        if str(temp_issue[0]) == str(request.form["hide_id"]):
            temp_issue.append("selected")
            list_select.append(temp_issue)
        else:
            temp_issue.append(" ")
            list_select.append(temp_issue)

    return render_template("custom_reference_remove.html",
                           issue_list=list_select,
                           reference_list=list_reference,
                           input_id=request.form["hide_id"])


@flask_app.route("/select_issue", methods=["POST"])
def select_test():
    list_issues = sql_db.read_data_issues('db/test.db')
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
    return render_template("custom_issue_edit.html",
                           issue_list=list_select,
                           input_origin=single_issue[0],
                           input_score=single_issue[1],
                           input_weight=single_issue[2],
                           input_cost=single_issue[3],
                           input_name_zh=single_issue[4],
                           input_name_en=single_issue[5],
                           input_desc_zh=single_issue[6],
                           input_desc_en=single_issue[7],
                           input_solu_zh=single_issue[8],
                           input_solu_en=single_issue[9],
                           input_id=request.form["issue_id"])


@flask_app.route("/select_issue_issue_type", methods=["POST"])
def select_issue_issue_type():
    list_issues = sql_db.read_data_issues('db/test.db')
    list_type = sql_db.read_data('db/test.db', 'TYPE')
    list_select = []
    for issue in list_issues:
        temp_issue = list(issue)
        if str(temp_issue[0]) == str(request.form["issue_id"]):
            temp_issue.append("selected")
            list_select.append(temp_issue)
        else:
            temp_issue.append(" ")
            list_select.append(temp_issue)

    return render_template("custom_issue_type.html",
                           issue_list=list_select,
                           type_list=list_type,
                           hide_issue=request.form["issue_id"])


@flask_app.route("/select_type_issue_type", methods=["POST"])
def select_type_issue_type():
    list_issues = sql_db.read_data_issues('db/test.db')
    list_type = sql_db.read_data('db/test.db', 'TYPE')
    type_name = sql_db.read_list_by_id('db/test.db', request.form["type_id"])
    list_item = sql_db.read_data('db/test.db', type_name)
    list_select_issue = []
    list_select_type = []
    for issue in list_issues:
        temp_issue = list(issue)
        if str(temp_issue[0]) == str(request.form["hide_issue"]):
            temp_issue.append("selected")
            list_select_issue.append(temp_issue)
        else:
            temp_issue.append(" ")
            list_select_issue.append(temp_issue)

    for temp_type in list_type:
        temp_type = list(temp_type)
        if str(temp_type[0]) == str(request.form["type_id"]):
            temp_type.append("selected")
            list_select_type.append(temp_type)
        else:
            temp_issue.append(" ")
            list_select_type.append(temp_type)

    return render_template("custom_issue_type.html",
                           issue_list=list_select_issue,
                           type_list=list_select_type,
                           item_list=list_item,
                           hide_issue=request.form["hide_issue"],
                           hide_type=request.form["type_id"])




@flask_app.route("/select_issue_tag", methods=["POST"])
def select_issue_tag():
    list_issues = sql_db.read_data_issues('db/test.db')
    # list_tag = sql_db.read_tag_by_id('db/test.db', request.form["issue_id"])
    list_select = []
    for issue in list_issues:
        temp_issue = list(issue)
        if str(temp_issue[0]) == str(request.form["issue_id"]):
            temp_issue.append("selected")
            list_select.append(temp_issue)
        else:
            temp_issue.append(" ")
            list_select.append(temp_issue)

    return render_template("custom_tag_add.html",
                           issue_list=list_select,
                           tag_list=list_tag,
                           input_id=request.form["issue_id"])


@flask_app.route("/select_reference_tag", methods=["POST"])
def select_reference_tag():
    list_issues = sql_db.read_data_issues('db/test.db')
    list_reference = sql_db.read_reference_by_id('db/test.db', request.form["issue_id"])
    list_select = []
    for issue in list_issues:
        temp_issue = list(issue)
        if str(temp_issue[0]) == str(request.form["issue_id"]):
            temp_issue.append("selected")
            list_select.append(temp_issue)
        else:
            temp_issue.append(" ")
            list_select.append(temp_issue)

    return render_template("custom_reference_add.html",
                           issue_list=list_select,
                           reference_list=list_reference,
                           input_id=request.form["issue_id"])


@flask_app.route("/select_issue_tag_remove", methods=["POST"])
def select_issue_tag_remove():
    list_issues = sql_db.read_data_issues('db/test.db')
    list_tag = sql_db.read_tag_by_id('db/test.db', request.form["issue_id"])
    list_select = []
    for issue in list_issues:
        temp_issue = list(issue)
        if str(temp_issue[0]) == str(request.form["issue_id"]):
            temp_issue.append("selected")
            list_select.append(temp_issue)
        else:
            temp_issue.append(" ")
            list_select.append(temp_issue)

    return render_template("custom_tag_remove.html",
                           issue_list=list_select,
                           tag_list=list_tag,
                           input_id=request.form["issue_id"])


@flask_app.route("/select_issue_reference_remove", methods=["POST"])
def select_issue_reference_remove():
    list_issues = sql_db.read_data_issues('db/test.db')
    list_reference = sql_db.read_reference_by_id('db/test.db', request.form["issue_id"])
    list_select = []
    for issue in list_issues:
        temp_issue = list(issue)
        if str(temp_issue[0]) == str(request.form["issue_id"]):
            temp_issue.append("selected")
            list_select.append(temp_issue)
        else:
            temp_issue.append(" ")
            list_select.append(temp_issue)

    return render_template("custom_reference_remove.html",
                           issue_list=list_select,
                           reference_list=list_reference,
                           input_id=request.form["issue_id"])


@flask_app.route("/select_tag", methods=["POST"])
def select_tag():
    list_issues = sql_db.read_data_issues('db/test.db')
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
    for i in list_select:
        print(str(i))
    return render_template("custom_issue_edit.html",
                           issue_list=list_select,
                           input_origin=single_issue[0],
                           input_score=single_issue[1],
                           input_weight=single_issue[2],
                           input_cost=single_issue[3],
                           input_name_zh=single_issue[4],
                           input_name_en=single_issue[5],
                           input_desc_zh=single_issue[6],
                           input_desc_en=single_issue[7],
                           input_solu_zh=single_issue[8],
                           input_solu_en=single_issue[9],
                           input_id=request.form["issue_id"])


@flask_app.route("/index", methods=["GET"])
@login_required
def index():
    temp_issues = sql_db.read_data_issues('db/test.db')
    return render_template("custom_index.html", issue_list=reversed(temp_issues))


@flask_app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(flask_app.root_path, "static"),
                               "favicon.ico",
                               mimetype="image/vnd.microsoft.icon")


# 3. error handle
@flask_app.errorhandler(404)
def page_not_found(e):
    return redirect("/index")


# 3. main
def create_app():
    # unit_test_report()
    update_user()
    flask_app.debug = True
    flask_app.run(host="0.0.0.0", port=8124, debug=False)
