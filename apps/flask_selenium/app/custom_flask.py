from flask import (
    Flask,
    send_from_directory,
    redirect,
    render_template,
    request,
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
from werkzeug.utils import secure_filename
import time
import app.db.custom_sqlite as sql_db
import app.models.custom_auto_test as auto_test

# config init
config = configparser.ConfigParser()
config.read("config.ini")

# flask init
flask_app = Flask(__name__)
flask_app.secret_key = config.get("flask", "secret_key")
flask_app.config['UPLOAD_FOLDER'] = config.get("flask", "upload_folder")
allow_extension = {'py', 'jpg'}

# users list
users = {"onedegree": {"password": "onedegree9527"}}

# Flask-Login init
login_manager = LoginManager()
login_manager.init_app(flask_app)
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


@flask_app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        redirect("/")

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
        return render_template("custom_demo.html")
    return redirect("/login")


@flask_app.route("/index", methods=["GET"])
def index():
    temp_fields = ['NAME', 'DESCRIPTION', 'FILE', 'KEYWORD', 'STATUS', 'ACTION']
    temp_column = sql_db.read_data('app/db/test.db', 'TESTCASE')
    return render_template("custom_index.html",
                           labels=temp_fields,
                           column_testcase=temp_column)


@flask_app.route("/demo", methods=["GET", "POST"])
@login_required
def demo():
    print(current_user.id)
    temp_fields = ['NAME', 'DESCRIPTION', 'FILE', 'KEYWORD', 'STATUS', 'ACTION']
    temp_column = sql_db.read_data('app/db/test.db', 'TESTCASE')
    return render_template("custom_demo.html",
                           labels=temp_fields,
                           column_testcase=temp_column)


@flask_app.route("/shell", methods=["GET"])
@login_required
def shell():
    with open('temp/test.txt', 'a') as temp_file:
        temp_lines = ['']
        try:
            temp_lines = temp_file.readlines()
        except Exception as ex:
            print('Exception:' + str(ex))

    return render_template("custom_shell.html", result_list=temp_lines)


@flask_app.route("/shell", methods=["POST"])
@login_required
def shell_post():
    print(request.form['html_input'])
    # app.models.api_shell.run()
    api_shell.run(request.form['html_input'], 'temp/test.txt')
    temp_lines = []
    with open('temp/test.txt') as temp_file:
        temp_lines = temp_file.readlines()
    return render_template("custom_shell.html", result_list=temp_lines)


@flask_app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(flask_app.root_path, "static"),
                               "favicon.ico",
                               mimetype="image/vnd.microsoft.icon")


@flask_app.route("/temp/<image_id>", methods=["POST"])
def result_img(image_id):
    return send_from_directory(os.path.join(flask_app.root_path, "../temp"), image_id + '.png')


@flask_app.errorhandler(404)
def page_not_found(e):
    return redirect("/index")


def create_new_testcase(input_id, file_name):
    real_name_list = file_name.split('_')
    class_name = real_name_list[0].capitalize() + real_name_list[1].capitalize()
    temp_list = [f"        if input_id == '{input_id}':\n",
                 f"            import app.upload.{file_name}\n",
                 f"            test = app.upload.{file_name}.{class_name}()\n",
                 f"            test.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())\n",
                 f"            time.sleep(1)\n",
                 f"            test.{file_name}()\n",
                 f"            temp_result = test.driver.page_source\n",
                 f"            test.driver.save_screenshot(input_id + '.png')\n",
                 f"            test.teardown_method('test')\n",
                 f"            print(\"testcase:\" + \"{input_id}\")\n"]
    return temp_list


@login_required
@flask_app.route('/upload', methods=['POST'])
def uploaded_file():
    import app.utils.custom_file
    file = request.files['file']
    name = request.form['name_title']
    desc = request.form['name_desc']
    verify = request.form['name_verify']
    if file:
        filename = secure_filename(file.filename)
        print(flask_app.config['UPLOAD_FOLDER'])
        if os.path.isdir(flask_app.config['UPLOAD_FOLDER']):
            file.save(os.path.join(flask_app.config['UPLOAD_FOLDER'], filename))
            print("upload success")
            print(current_user.id)
            filename_only = app.utils.custom_file.read_name(filename)
            sql_db.add_testcase('app/db/test.db', name, desc, filename_only, verify, current_user.id)
            time.sleep(3)
            sql_id = app.db.custom_sqlite.read_testcase_id('app/db/test.db', name)
            print('sql_id:' + str(sql_id))
            temp_list = create_new_testcase(sql_id, filename_only)
            app.utils.custom_file.add_lines('app/models/custom_auto_test.py', temp_list, '# auto testcase end')
        else:
            print("folder not exist, please check config")
    else:
        print("upload file is null")
    return redirect("/demo")


@flask_app.route("/run/<button_temp>", methods=["POST"])
def run_testcase(button_temp):
    button = str(button_temp)
    count_list = button.split('_')
    result = auto_test.select_test(count_list[-1])
    verify = app.db.custom_sqlite.read_verify_by_id('app/db/test.db', count_list[-1])
    status = check_response(result, verify)
    app.db.custom_sqlite.update_status_by_id('app/db/test.db', count_list[-1], str(status))
    if os.path.isfile(count_list[-1] + '.png'):
        os.rename(count_list[-1] + '.png', './temp/' + count_list[-1] + '.png')
    print("run:" + button)
    print("verify:" + verify)
    print('result:' + result)
    print('status:' + str(status))
    return redirect("/demo")


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


def create_app():
    flask_app.debug = True
    flask_app.run(host="0.0.0.0", port=8123, debug=False)
