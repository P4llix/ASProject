from flask import Flask, redirect, render_template, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from queries import *
from forms import *

SQL_DIALECT = "mysql"
PYTHON_DB_API = "pymysql"
DB_IP = "root@localhost"
DB_NAME = "as_projekt"


engine = create_engine(f"{SQL_DIALECT}+{PYTHON_DB_API}://{DB_IP}/{DB_NAME}")
db = engine.connect()

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
    'unit' : Base.classes.unit
}
db = Database(sess, table)


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcache'
app.config['SECRET_KEY'] = 'tajnykod'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




@app.route('/')
def index():
    daily_task_dates = db.daily_task_all()
    daily_task_groupby = []

    for daily_task_date in daily_task_dates:
        daily_task_groupby.append(db.daily_task_specific(daily_task_date.DATE))
    print(daily_task_groupby)

    return render_template("index.html", tasks = daily_task_groupby)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    return render_template('login.html', form = form)





# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm(request.form)
#     if form.submit() and form.validate():
#         password = form.password.data.encode('utf-8')
#         password = hashlib.md5(password).hexdigest()
#         usr = form.username.data
#         print(usr)
#         print(password)

#         # res = login_first(sess, User, str(usr), str(password))
#         # res = sess.query(User).first()#.filter_by(Login = usr, Password = password)
#         # sql = text(f'SELECT * FROM User WHERE Username = {usr} AND Password = {password}')
#         # res = sess.execute(sql)

#         # res = sess.query(User).from_statement(sqlalchemy.text("Select * from User WHERE Login = :l AND Password = :p")).params(l = usr, p = password).first()
#         res = log(usr, password)
#         # if res:
#         #     print(res.Username)
#         return redirect(url_for('home'))

#         # if res:
#         #     session['logged'] = True
#         #     # print("res: "+res)
#         #     # session['UserID'] = res.User_ID
#         #     flash('Sucessfull logged')
#         #     return redirect(url_for('home'))
            
#     return render_template("login.html", form = form)


# @app.route('/')
# def index(): 
#     return render_template("index.html")
    

if __name__ == '__main__':
    app.run(debug=True)
