from functools import wraps
from flask import Flask, jsonify, redirect, render_template, url_for, flash, request, session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from queries import *
from forms import *
from User import *
from ECC import *
import hashlib as hsl
from flask_paginate import Pagination, get_page_parameter
from flask_mail import Mail, Message
import random



SQL_DIALECT = "mysql"
PYTHON_DB_API = "pymysql"
DB_IP = "root@localhost"
DB_NAME = "as_projekt"
PRIVATE_KEY = 0x63bd3b01c5ce749d87f5f7481232a93540acdb0f7b5c014ecd9cd32b041d6f33


engine = create_engine(f"{SQL_DIALECT}+{PYTHON_DB_API}://{DB_IP}/{DB_NAME}")
db_engine = engine.connect()

Base = automap_base()
Base.prepare(engine, reflect=True)
sess = scoped_session(sessionmaker(engine))

table = {
    'credential' : Base.classes.credential,
    'daily_task' : Base.classes.daily_task,
    'exercise' : Base.classes.exercise,
    'role' : Base.classes.role,
    'task' : Base.classes.task,
    'user' : Base.classes.user,
    'user_daily_task' : Base.classes.user_daily_task,
    'user_role' : Base.classes.user_role,
    'unit' : Base.classes.unit,
    'settings' : Base.classes.setup
}
db = Database(sess, table)
user = User(db)


settings_raw = db.get_settings()
settings = {}
for setting in settings_raw:
    settings[setting.NAME] = setting.VALUE

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcache'
app.config['SECRET_KEY'] = 'tajnykod'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = settings['MAIL_SERVER']
app.config['MAIL_PORT'] = settings['MAIL_PORT']
app.config['MAIL_USERNAME'] = settings['MAIL_ADRESS']
app.config['MAIL_PASSWORD'] = settings['MAIL_PASSWORD']
# app.config['MAIL_USE_TLS'] = bool(settings['MAIL_TLS'])
app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = bool(settings['MAIL_SSL'])
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
ecc = ECC(PRIVATE_KEY)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwagrs):
        if session.get('auth', 0) == 1:
            return f(*args, **kwagrs)
        else:
            flash('Potwierdź swoją tożsamość logując się')
            return redirect(url_for('login'))
    return wrap

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwagrs):
        if 'ADMIN' in user.roles and user.roles['ADMIN'] == 1 :
            return f(*args, **kwagrs)
        else:
            flash('Restricted area')
            return redirect(url_for('home'))
    return wrap

def mod_required(f):
    @wraps(f)
    def wrap(*args, **kwagrs):
        if 'MOD' in user.roles and user.roles['MOD'] == 1 :
            return f(*args, **kwagrs)
        else:
            flash('Restricted area')
            return redirect(url_for('home'))
    return wrap


@app.route('/api/user/update', methods = ['POST', 'GET'])
def api_user_update():
    if request.method == 'POST':
        user_data = {
            'rowid' : request.form['userid'],
            'firstname' : request.form['userimie'],
            'lastname' : request.form['usernazwisko'],
            'phone' : request.form['usertelefon'],
            'birthday' : request.form['userurodziny'],
            'email' : request.form['useremail'],
            'status' : request.form['userstatus'],
        }
        db.update_user(user_data)
        db.session.commit()
        return jsonify('')


@app.route('/api/user/add', methods = ['POST', 'GET'])
def api_user_add():
    if request.method == 'POST':
        user_data = {
            'firstname' : request.form['userimie'],
            'lastname' : request.form['usernazwisko'],
            'phone' : request.form['usertelefon'],
            'email' : request.form['useremail']
        }

        email_exists =  db.user_recognise(user_data['email'])
        if not user_data['email']:
            return jsonify(message='Pole email jest obowiązkowe'), 400
        if email_exists:
            return jsonify(message='Podany email już istnieje'), 400
        if '@' not in user_data['email']:
            return jsonify(message='Podano błędny składniowo email'), 400

        db_engine.execute(f" insert into USER (FIRSTNAME, LASTNAME, PHONE, EMAIL) values ('{user_data['firstname']}', '{user_data['lastname']}', '{user_data['phone']}', '{user_data['email']}') ")
        db.session.commit()

        user_id = db.user_recognise(user_data['email'])[0]
        hash = ecc.hash(random.random())

        db_engine.execute(f" insert into CREDENTIAL (USER, URL, PASSWORD) values ({user_id}, '{hash}', '{ecc.hash(random.random())}') ")
        db.session.commit()

        # mail_template = render_template(
        #     'mail.html', 
        #     firstname=user_data['firstname'],
        #     url_link=hash
        # )

        # msg = Message('Utwórz hasło', sender = settings['MAIL_ADRESS'], recipients = [str(user_data['email'])])
        # msg.html = mail_template
        # mail.send(msg)

        

        return jsonify('')

@app.route('/api/user/remove', methods = ['POST', 'GET'])
def api_user_remove():
    if request.method == 'POST':
        user_id = request.form['userid']
        db_engine.execute(f"delete from user where ROWID = {user_id}")
        db_engine.execute(f"delete from credential where USER = {user_id}")
        db_engine.execute(f"delete from user_role where USER = {user_id}")
        db_engine.execute(f"delete from user_daily_task where USER = {user_id}")
        db.session.commit()
        return jsonify('')


@app.route('/api/user/get', methods = ['POST', 'GET'])
def api_user_get():
    if request.method == 'POST':
        userid = request.form['userid']
        user_data = db.user_specific(userid)

        return jsonify([
            userid, 
            user_data.FIRSTNAME, 
            user_data.LASTNAME, 
            user_data.PHONE, 
            user_data.EMAIL,
            True if user_data.STATUS else False,
            user_data.BIRTHDAY.strftime("%Y-%m-%d") if user_data.BIRTHDAY and user_data.BIRTHDAY not in ('0000-00-00', 'None', '0') else ''
        ])


@app.route('/api/role/get', methods = ['POST', 'GET'])
def api_get_role():
    if request.method == 'POST':
        userid = request.form['userid']
        user_roles = {
            'ADMIN' : db.user_role_status(userid, 'ADMIN'),
            'MOD' : db.user_role_status(userid, 'MOD'),
            'USER' : db.user_role_status(userid, 'USER')
        }

        data = ''
        for role, status in user_roles.items():
            data += f'<div class="input-group input-group-sm mb-4">  \
                        <span class="input-group-text" id="rowid">{role}</span>\
                        <input type="checkbox" id="userRole{role}"{("checked" if status == 1 else "")}>\
                    </div>'

        data += f'<input type="hidden" id="userid" value="{userid}">'
        return jsonify(data)

@app.route('/api/role/update', methods = ['POST', 'GET'])
def api_role_update():
    if request.method == 'POST':
        userid = request.form['userid']
        role_data = {
            1 : request.form['statusAdmin'],
            2 : request.form['statusUser'],
            3 : request.form['statusMod']
        }

        for role, status in role_data.items():
            db_engine.execute(f'insert into USER_ROLE (USER, ROLE, STATUS) values ({userid},{role},{status})')
            db.session.commit()

        return jsonify('')


@app.route('/api/unit/insert', methods = ['POST', 'GET'])
def api_unit_insert():
    if request.method == 'POST':
        unit_name = request.form['unit_name']

        db_engine.execute(f"insert into UNIT (NAME) values ('{unit_name}')")
        db.session.commit()
        return jsonify('')


@app.route('/api/exercise/insert', methods = ['POST', 'GET'])
def api_exercise_insert():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        link = request.form['link']

        db_engine.execute(f"insert into EXERCISE (NAME, DESCRIPTION, LINK) values ('{name}','{desc}','{link}')")
        db.session.commit()
        return jsonify('')


@app.route('/api/exercise/get', methods = ['POST', 'GET'])
def api_exercise_get():
    if request.method == 'POST':
        id = request.form['id']

        result = db.exercise_specific(id)
        db.session.commit()

        return jsonify([result.ROWID, result.NAME, result.DESCRIPTION, result.LINK])


@app.route('/api/exercise/update', methods = ['POST', 'GET'])
def api_exercise_update():
    if request.method == 'POST':
        data = {
            'id' :request.form['id'],
            'name' : request.form['nazwa'],
            'description' : request.form['opis'],
            'link' : request.form['link']
        }

        db.update_exercise(data)
        db.session.commit()

        return jsonify('')



@app.route('/api/task/insert', methods = ['POST', 'GET'])
def api_task_add():
    if request.method == 'POST':
        data = {
            'exercise' : request.form['exercise'],
            'quantity' : request.form['quantity'],
            'comment' : request.form['comment'],
            'unit' : request.form['unit']
        }
        db_engine.execute(f" insert into TASK (EXERCISE, QUANTITY, COMMENT, UNIT) values ('{data['exercise']}', '{data['quantity']}', '{data['comment']}', '{data['unit']}') ")
        db.session.commit()
        return jsonify('')


@app.route('/api/task/get', methods = ['POST', 'GET'])
def api_task_get():
    if request.method == 'POST':
        taskid = request.form['taskid']
        result = db.task_specific(taskid)

        return jsonify([
                result.ROWID,
                result.EXERCISE,
                result.QUANTITY,
                result.COMMENT,
                result.UNIT
            ])


@app.route('/api/task/update', methods = ['POST', 'GET'])
def api_task_update():
    if request.method == 'POST':
        data = {
            'id' : request.form['taskid'],
            'exercise' : request.form['exercise'],
            'quantity' : request.form['quantity'],
            'unit' : request.form['unit'],
            'comment' : request.form['comment']
        }

        db.update_task(data)
        db.session.commit()

        return jsonify('')



@app.route('/api/daily/insert', methods = ['POST', 'GET'])
def api_daily_insert():
    if request.method == 'POST':
        data = {
            'task' : request.form['task'],
            'comment' : request.form['comment'],
            'date' : request.form['date'],
            'users' : request.form['users'],
            'author' : request.form['author'],
            'id' : request.form['dailyid']
        }
        mode = int(request.form['mode'])

        if not data['users']:
            return jsonify(message='Nie wybrano uczestników'), 400
        data['users'] = data['users'].split(';')

        if not data['task']:
            return jsonify(message='Nie podano zadania'), 400

        if not data['date']:
            return jsonify(message='Nie podano daty'), 400


        if mode == 0:
            tasks_on_date = db.daily_task_on_date(data['date'])
            for task in tasks_on_date:
                if int(task.TASK) == int(data['task']):
                    return jsonify(message='Zadanie jest już zaplanowane na podaną date'), 400
        
            db_engine.execute(f" insert into DAILY_TASK (AUTHOR, TASK, DATE, COMMENT) values ({data['author']}, {data['task']}, '{data['date']}', '{data['comment']}') ")
            db.session.commit()

            dailytask = db.daily_task_recognise({'author':data['author'], 'task':data['task'], 'date':data['date']})
            for user in data['users']:
                user = int(user)
                db_engine.execute(f" insert into USER_DAILY_TASK (USER, DAILY_TASK) values ({user}, {dailytask.ROWID}) ")
                db.session.commit()

        if mode == 1:
            new_users = [int(v) for v in data['users']]
            existing = [int(v[0]) for v in db.user_daily_group(data['id'])]
            dailytask = db.daily_task_recognise({'author':data['author'], 'task':data['task'], 'date':data['date']})

            for user in new_users:
                if user not in existing:
                    response = db.check_if_user_exist(data['id'], user)
                    if not response:
                        db_engine.execute(f" insert into USER_DAILY_TASK (USER, DAILY_TASK) values ({user}, {dailytask.ROWID}) ")
                        db.session.commit()


            for user in existing:
                if user not in new_users:
                    response = db.check_if_user_exist(data['id'], user)
                    if response and response[0][0] > 0:
                        db_engine.execute(f"delete from USER_DAILY_TASK where ROWID = {response[0][0]}")
                        db.session.commit()
                        pass

        return jsonify('')


@app.route('/api/daily/users', methods = ['POST', 'GET'])
def api_daily_users():
    if request.method == 'POST':
        final_users = []
        users = db.all_users()

        for user in users:
            role_status = db.user_role_status(user.ROWID, 'USER')
            if role_status:
                final_users.append(user)

        records = ''
        for idx, user in enumerate(final_users):
            records += f'<tr><td><label for="box{idx}">{user.FIRSTNAME} {user.LASTNAME}</td><td><input type="checkbox" class="usersDaily" value="{user.ROWID}" id="box{idx}" {"checked" if user.STATUS else ""}></td></tr>'
        return jsonify(records)


@app.route('/api/mark/get/date', methods = ['POST', 'GET'])
def api_mark_get_date():
    if request.method == 'POST':
        dates = db.daily_task_on_date(request.form['date'])
        result = []
        for date in dates:
            task = db.task_specific_full(date.TASK)
            result.append([task.ROWID, task.EXERCISE_NAME, task.QUANTITY, task.UNIT_NAME, date.ROWID])
        return jsonify(result)


@app.route('/api/mark/get/users', methods = ['POST', 'GET'])
def api_mark_get_users():
    if request.method == 'POST':
        id = request.form['dailyid']
        users = db.daily_task_users(id)
        result = []

        for user in users:
            result.append([user.ROWID, user.FIRSTNAME, user.LASTNAME, str(id)])
            
        return jsonify(result)


@app.route('/api/mark/get/user', methods = ['POST', 'GET'])
def api_mark_get_user():
    if request.method == 'POST':
        dailyid = request.form['dailyid']
        userid = request.form['userid']
        user = db.daily_task_user(dailyid, userid)
            
        return jsonify([user.LINK, user.MARK, user.FIRSTNAME, user.LASTNAME, user.COMMENT, dailyid, userid])


@app.route('/api/mark/update/user', methods = ['POST', 'GET'])
def api_mark_update_user():
    if request.method == 'POST':
        data = {
            'mark': request.form['mark'],
            'comment': request.form['comment'],
            'dailyid': request.form['dailyid'],
            'userid': request.form['userid']
        }
        db.daily_task_user_update(data)
        db.session.commit()
        return jsonify('')


@app.route('/api/daily/detail', methods = ['POST', 'GET'])
def api_daily_detail():
    if request.method == 'POST':
        dailyid = request.form['dailyid']

        daily = db.daily_task_specific(dailyid)
        return jsonify([daily.TASK, daily.DATE.strftime("%Y-%m-%d"), daily.COMMENT, daily.ROWID])


@app.route('/api/daily/user/get', methods = ['POST', 'GET'])
def api_daily__user_get():
    if request.method == 'POST':
        id = request.form['dailyid']
        result = db.daily_task_users(id)
        records = ''

        for user in result:
            stars = []
            mark = user.MARK if user.MARK in range(0, 6) else -1
            if mark > -1:
                stars = ["<span class=\"fa fa-star star-checked\"></span>" for _ in range(0, mark)]

            for _ in range(0, 5-mark):
                stars.append("<span class=\"fa fa-star\"></span>")

            records += f'<tr><td>{user.FIRSTNAME}</td><td>{user.LASTNAME}</td><td>{" ".join(stars) if mark != -1 else "-"}</td></tr>'

        return jsonify(records)


@app.route('/api/daily/link/update', methods = ['POST', 'GET'])
def api_daily_link():
    if request.method == 'POST':
        link = request.form['link']
        userid = request.form['userid']
        dailyid = request.form['dailyid']

        print(userid, dailyid, link)
        db.user_link_update(userid, dailyid, link)
        db.session.commit()

        return jsonify('')
        
@app.route('/')
def index():
    daily_task_dates = db.daily_task_all()
    daily_task_groupby = []

    for daily_task_date in daily_task_dates:
        daily_task_groupby.append(db.daily_task_specific_day(daily_task_date.DATE))

    return render_template("index.html", tasks = daily_task_groupby)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    password = form.password.data.encode('utf-8')
    login = form.login.data

    # if submited
    if form.submit() and password and login:

        confirmed = db.auth(login, hsl.md5(password).hexdigest())

        if confirmed:
            session['id'] = confirmed.USER
            session['auth'] = 1
            flash('Poprawnie zalogowano')
            return redirect(url_for('home'))
        else:
            flash('Niepoprawne dane logowania')
            return redirect(url_for('login'))

    # if not print login
    return render_template('login.html', form = form)

@app.route('/home')
@login_required
def home():
    # feed user object
    user.set_id(session.get('id'))
    user.set_personal()
    user.get_roles()

    all_user_task = db.user_daily_task_specific_user(user.id)
    
    return render_template('home.html', user = user, tasks = all_user_task)


@app.route('/home/admin/task')
@admin_required
@login_required
def administration_task():
    units_all = db.all_units()
    exercise_all = db.all_exercise()
    tasks_all = db.all_tasks()
    daily_task_all = db.all_daily_task()

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    if page != None:
        x = (int(page) - 1) * per_page
        y = int(page) * per_page

    pagination = Pagination(page=page, total=len(daily_task_all), search=False, record_name='')    

    return render_template(
        'administration_task.html', 
        user = user,
        units = units_all,
        exercises = exercise_all,
        tasks = tasks_all,
        daily_tasks = daily_task_all[x:y],
        pagination = pagination
    )


@app.route('/home/admin/user')
@admin_required
@login_required
def administration_user():
    all_users = db.all_users()
    page = request.args.get(get_page_parameter(), type=int, default=1)

    per_page = 10
    if page != None:
        x = (int(page) - 1) * per_page
        y = int(page) * per_page

    pagination = Pagination(page=page, total=len(all_users), search=False, record_name='users')

    return render_template(
        'administration_user.html', 
        user = user, 
        users = all_users[x:y],
        pagination = pagination
    )



@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Pomyślnie wylogowano')
    return redirect(url_for('login'))


@app.route('/activation/<url>', methods=['GET', 'POST'])
def password_create(url):
    form = LoginForm(request.form)
    new_password = form.new_password.data.encode('utf-8')
    confirmation = form.confirm.data.encode('utf-8')

    if new_password and confirmation:
        if new_password == confirmation:
            data = {
                'url': url,
                'password': hsl.md5(new_password).hexdigest()
            }

            db.credential_update(data)
            db.session.commit()

            flash('Poprawnie ustawiono hasło!')
            return redirect(url_for('login'))
        else:
            flash('Podane hasła nie są takie same')
            return render_template('password.html', form = form)

    return render_template('password.html', form = form)


@app.route('/home/archiwum', methods=['GET', 'POST'])
def archive():
    print(user.rowid)
    rows = db.user_daily_task_user(user.rowid)
    print(rows)

    return render_template(
        'archive.html', 
        user = user,
        rows = rows
    )


@app.route('/home/moderation/mark')
@mod_required
@login_required
def moderation_mark():
    return render_template(
        'moderation_mark.html',
        user = user
    )


if __name__ == '__main__':
    app.run(debug=True)
