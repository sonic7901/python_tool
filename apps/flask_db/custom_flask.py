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
    list_user = sql_db.read_data('USER')
    # list_user = sql_db.read_data_users('db/test.db')
    for temp_user in list_user:
        users[temp_user[1]] = {'password': temp_user[2]}


@flask_app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/index")
    if request.method == "GET":
        return render_template("custom_login.html", html_hint="請輸入帳號密碼")

    user_id = request.form["user_id"]
    user_id = str(user_id)
    if len(user_id) > 64 or len(user_id) == 0:
        return render_template("custom_login.html", html_hint="帳號或密碼錯誤")
    elif (user_id in users) and (request.form["password"] == users[user_id]["password"]):
        user = User()
        user.id = user_id
        login_user(user)
        return redirect("/index")
    return render_template("custom_login.html", html_hint="帳號或密碼錯誤")


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


@flask_app.route("/button_issue_add", methods=["POST"])
def button_add():
    '''
    sql_db.add_issue('db/test.db',
                     request.form['origin_name'],
                     request.form['issue_weight'],
                     request.form['issue_cost'],
                     request.form['name_en'],
                     request.form['name_zh'],
                     request.form['desc_en'],
                     request.form['desc_zh'],
                     request.form['solu_en'],
                     request.form['solu_zh'])
    '''
    new_id = sql_db.add_issue(request.form['issue_score'], request.form['issue_weight'], request.form['issue_cost'])
    if not new_id == 0:
        sql_db.add_issue_name(new_id, 1, request.form['name_en'])
        sql_db.add_issue_name(new_id, 2, request.form['name_zh'])
        sql_db.add_issue_description(new_id, 1, request.form['desc_en'])
        sql_db.add_issue_description(new_id, 2, request.form['desc_zh'])
    return redirect("/index")


@flask_app.route("/issue_edit")
def issue_edit():
    temp_issues = sql_db.read_data('ISSUE')
    show_list = []
    for temp_issue in temp_issues:
        temp_name = sql_db.read_data_issue_name(temp_issue[0], 2)
        show_list.append([temp_issue[0], temp_name])
    return render_template("custom_issue_edit.html", issue_list=show_list)


@flask_app.route("/button_issue_edit", methods=["POST"])
def button_edit():
    show_list = []
    list_issues = sql_db.read_data('ISSUE')
    if str(request.form['hide_id']) == '':
        for temp_issue in list_issues:
            temp_name = sql_db.read_data_issue_name(temp_issue[0], 2)
            show_list.append([temp_issue[0], temp_name])
        return render_template("custom_issue_edit.html", issue_list=show_list, temp_label="請先選擇要修改的 issue")
    else:
        list_issues = sql_db.read_data('ISSUE')
        print("hide_id:" + request.form["hide_id"])
        show_list = []
        for temp_issue in list_issues:
            temp_name = sql_db.read_data_issue_name(temp_issue[0], 2)
            if str(temp_issue[0]) == str(request.form['hide_id']):
                show_list.append([temp_issue[0], temp_name, 'selected'])
            else:
                show_list.append([temp_issue[0], temp_name, ' '])
        sql_db.update_issue(request.form['hide_id'],
                            request.form['issue_score'],
                            request.form['issue_weight'],
                            request.form['issue_cost'])
        sql_db.update_issue_name(request.form['hide_id'], 2, request.form['name_zh'])
        sql_db.update_issue_name(request.form['hide_id'], 1, request.form['name_en'])
        sql_db.update_issue_description(request.form['hide_id'], 2, request.form['desc_zh'])
        sql_db.update_issue_description(request.form['hide_id'], 1, request.form['desc_en'])
        select_issue = list_issues[int(request.form["hide_id"]) - 1]
        return render_template("custom_issue_edit.html",
                               issue_list=show_list,
                               input_score=request.form['issue_score'],
                               input_weight=request.form['issue_weight'],
                               input_cost=request.form['issue_cost'],
                               input_name_zh=sql_db.read_data_issue_name(select_issue[0], 2),
                               input_name_en=sql_db.read_data_issue_name(select_issue[0], 1),
                               input_desc_zh=sql_db.read_data_issue_description(select_issue[0], 2),
                               input_desc_en=sql_db.read_data_issue_description(select_issue[0], 1),
                               input_id=request.form["hide_id"])


@flask_app.route("/issue_remove")
def issue_remove():
    temp_issues = sql_db.read_data('ISSUE')
    show_list = []
    for temp_issue in temp_issues:
        temp_name = sql_db.read_data_issue_name(temp_issue[0], 2)
        show_list.append([temp_issue[0], temp_name])
    return render_template("custom_issue_remove.html", issue_list=show_list)


@flask_app.route("/button_issue_remove", methods=["POST"])
def button_remove():
    sql_db.delete_issue(request.form["issue_id"])
    return redirect("/index")


@flask_app.route("/solution_add")
def solution_add():
    return render_template("custom_solution_add.html")


@flask_app.route("/button_solution_add", methods=["POST"])
def button_solution_add():
    temp_result_en = sql_db.add_solution(request.form['name_en'], 1, request.form['solution_en'])
    temp_result_zh = sql_db.add_solution(request.form['name_zh'], 2, request.form['solution_zh'])
    if temp_result_en == 0 or temp_result_zh == 0:
        print("button_advice_add : error")
    return redirect("/index")


@flask_app.route("/solution_edit")
def solution_edit():
    temp_solutions = sql_db.read_data('ADVICE')
    show_list = []
    for temp_solution in temp_solutions:
        if temp_solution[2] == 2:
            show_list.append([temp_solution[0], temp_solution[1]])
    return render_template("custom_solution_edit.html", advice_list=show_list)


@flask_app.route("/solution_edit_select", methods=["POST"])
def solution_edit_select():
    temp_advices = sql_db.read_data('ADVICE')
    show_list = []
    for temp_advice in temp_advices:
        if temp_advice[2] == 2:
            if str(temp_advice[0]) == str(request.form['advice_id']):
                show_list.append([temp_advice[0], temp_advice[1], 'selected'])
            else:
                show_list.append([temp_advice[0], temp_advice[1], ' '])
    return render_template("custom_solution_edit.html",
                           advice_list=show_list,
                           input_name_zh=sql_db.read_data_advice_name(int(request.form['advice_id'])),
                           input_name_en=sql_db.read_data_advice_name(int(request.form['advice_id']) - 1),
                           input_solution_zh=sql_db.read_data_advice_display(int(request.form['advice_id'])),
                           input_solution_en=sql_db.read_data_advice_display(int(request.form['advice_id']) - 1),
                           input_id=str(request.form['advice_id']))


@flask_app.route("/button_solution_edit", methods=["POST"])
def button_solution_edit():
    print(request.form['hide_id'])
    print(request.form['name_en'])
    print(request.form['solution_en'])
    temp_result_en = sql_db.update_solution(int(request.form['hide_id']) - 1, request.form['name_en'], 1, request.form['solution_en'])
    temp_result_zh = sql_db.update_solution(int(request.form['hide_id']), request.form['name_zh'], 2, request.form['solution_zh'])
    if temp_result_en == 0 or temp_result_zh == 0:
        print("button_advice_add : error")
    temp_advices = sql_db.read_data('ADVICE')
    show_list = []
    for temp_advice in temp_advices:
        if temp_advice[2] == 2:
            if str(temp_advice[0]) == str(request.form['hide_id']):
                show_list.append([temp_advice[0], temp_advice[1], 'selected'])
            else:
                show_list.append([temp_advice[0], temp_advice[1], ' '])
    return render_template("custom_solution_edit.html",
                           advice_list=show_list,
                           input_name_zh=sql_db.read_data_advice_name(int(request.form['hide_id'])),
                           input_name_en=sql_db.read_data_advice_name(int(request.form['hide_id']) - 1),
                           input_solution_zh=sql_db.read_data_advice_display(int(request.form['hide_id'])),
                           input_solution_en=sql_db.read_data_advice_display(int(request.form['hide_id']) - 1),
                           input_id=str(request.form['hide_id']))


@flask_app.route("/solution_delete")
def solution_delete():
    temp_solution = sql_db.read_data('ADVICE')
    show_list = []
    for temp_advice in temp_solution:
        if temp_advice[2] == 2:
            show_list.append([temp_advice[0], temp_advice[1], ' '])
    return render_template("custom_solution_remove.html", advice_list=show_list)


@flask_app.route("/solution_delete_select", methods=["POST"])
def solution_delete_select():
    sql_db.delete_solution(request.form['advice_id'])
    sql_db.delete_solution(int(request.form['advice_id']) -1)
    temp_advices = sql_db.read_data('ADVICE')
    show_list = []
    for temp_advice in temp_advices:
        if temp_advice[2] == 2:
            if str(temp_advice[0]) == str(request.form['advice_id']):
                show_list.append([temp_advice[0], temp_advice[1], 'selected'])
            else:
                show_list.append([temp_advice[0], temp_advice[1], ' '])
    return render_template("custom_solution_remove.html", advice_list=show_list)


@flask_app.route("/solution_select")
def solution_select():
    temp_issues = sql_db.read_data('ISSUE')
    show_list_1 = []
    for temp_issue in temp_issues:
        temp_name = sql_db.read_data_issue_name(temp_issue[0], 2)
        show_list_1.append([temp_issue[0], temp_name])

    temp_solution = sql_db.read_data('ADVICE')
    show_list_2 = []
    for temp_advice in temp_solution:
        if temp_advice[2] == 2:
            show_list_2.append([temp_advice[0], temp_advice[1]])

    return render_template("custom_solution_select.html", issue_list=show_list_1, advice_list=show_list_2)


@flask_app.route("/button_solution_select", methods=["POST"])
def button_solution_select():
    # init
    show_list_1 = []
    show_list_2 = []
    try:
        temp_issue_id = int(request.form['issue_id'])
        temp_solution_id = int(request.form['advice_id'])
        temp_link_id = sql_db.read_link_advice(temp_solution_id)
        if sql_db.read_link_advice(temp_issue_id) == 0:
            sql_db.add_link_advice(temp_issue_id, temp_solution_id)
            sql_db.add_link_advice(temp_issue_id, temp_solution_id - 1)
        else:
            sql_db.update_link_advice(temp_issue_id, temp_solution_id)
            sql_db.update_link_advice(temp_issue_id, temp_solution_id - 1)

        temp_issues = sql_db.read_data('ISSUE')
        for temp_issue in temp_issues:
            temp_name = sql_db.read_data_issue_name(temp_issue[0], 2)
            show_list_1.append([temp_issue[0], temp_name])

        temp_solution = sql_db.read_data('ADVICE')
        for temp_advice in temp_solution:
            if temp_advice[2] == 2:
                show_list_2.append([temp_advice[0], temp_advice[1]])

    except Exception as ex:
        print('Exception:' + str(ex))

    return render_template("custom_solution_select.html", issue_list=show_list_1, advice_list=show_list_2)


@flask_app.route("/issue_type")
def issue_type():
    temp_issues = sql_db.read_data_issues('db/test.db')
    return render_template("custom_issue_type.html", issue_list=temp_issues, temp_label="請由上往下依序選擇")


@flask_app.route("/type_add")
def type_add():
    temp_types = sql_db.read_data('TYPE')
    return render_template("custom_type_add.html", type_list=temp_types)


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
    list_issues = sql_db.read_data('ISSUE')
    print("test:" + request.form["issue_id"])
    select_issue = list_issues[int(request.form["issue_id"]) - 1]
    show_list = []
    for temp_issue in list_issues:
        temp_name = sql_db.read_data_issue_name(temp_issue[0], 2)
        if str(temp_issue[0]) == str(request.form['issue_id']):
            show_list.append([temp_issue[0], temp_name, 'selected'])
        else:
            show_list.append([temp_issue[0], temp_name, ' '])
    return render_template("custom_issue_edit.html",
                           issue_list=show_list,
                           input_score=select_issue[1],
                           input_weight=select_issue[2],
                           input_cost=select_issue[3],
                           input_name_zh=sql_db.read_data_issue_name(select_issue[0], 2),
                           input_name_en=sql_db.read_data_issue_name(select_issue[0], 1),
                           input_desc_zh=sql_db.read_data_issue_description(select_issue[0], 2),
                           input_desc_en=sql_db.read_data_issue_description(select_issue[0], 1),
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
    temp_issues = sql_db.read_data('ISSUE')
    show_list = []
    for temp_issue in temp_issues:
        temp_name = sql_db.read_data_issue_name(temp_issue[0], 2)
        show_list.append([temp_issue[0], temp_name])
    return render_template("custom_index.html", issue_list=reversed(show_list))


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
    sql_db.set_db('db/test.db')
    update_user()
    flask_app.debug = True
    flask_app.run(host="0.0.0.0", port=8082, debug=False)
