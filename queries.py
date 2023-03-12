from sqlalchemy import desc


class Database:
    def __init__(self, sess, tables):
        self.session = sess
        self.tables = tables

    def user_select_all(self):
        user = self.tables['user']
        response = self.session.query(user).select_from(user).all()
        return response

    def daily_task_all(self):
        daily_task = self.tables['daily_task']
        response = self.session\
            .query(
                daily_task.DATE
            )\
            .select_from(daily_task)\
            .group_by(daily_task.DATE)\
            .order_by(desc(daily_task.DATE))
        return response

    def daily_task_specific_day(self, day):
        user = self.tables['user']
        daily_task = self.tables['daily_task']
        exercise =  self.tables['exercise']
        task =  self.tables['task']
        unit = self.tables['unit']

        response = self.session\
            .query(
                daily_task.ROWID, 
                user.FIRSTNAME,
                user.LASTNAME, 
                exercise.NAME, 
                task.QUANTITY, 
                daily_task.DATE,
                unit.NAME.label('UNIT')
            )\
            .select_from(daily_task)\
            .join(user, user.ROWID == daily_task.AUTHOR)\
            .join(task, task.ROWID == daily_task.TASK)\
            .join(exercise, exercise.ROWID == task.EXERCISE)\
            .join(unit, unit.ROWID == task.UNIT)\
            .where(daily_task.DATE == day)\
            .all()
        return response

    def daily_task_users(self, id):
        user = self.tables['user']
        user_daily_task = self.tables['user_daily_task']

        response = self.session\
            .query(
                user.FIRSTNAME,
                user.LASTNAME,
                user_daily_task.MARK,
                user_daily_task.LINK,
                user_daily_task.COMMENT,
                user.ROWID
            )\
            .select_from(user_daily_task)\
            .join(user, user.ROWID == user_daily_task.USER)\
            .where(user_daily_task.DAILY_TASK == id)\
            .order_by(user.FIRSTNAME,user.LASTNAME)\
            .all()
        return response

    def user_recognise(self, email):
        user = self.tables['user']

        response = self.session\
            .query(user.ROWID)\
            .select_from(user)\
            .where(user.EMAIL == email)\
            .first()
        return response

    def user_daily_task_specific_user(self, id):
        user = self.tables['user']
        daily_task = self.tables['daily_task']
        exercise =  self.tables['exercise']
        task =  self.tables['task']
        unit = self.tables['unit']
        user_daily_task = self.tables['user_daily_task']

        response = self.session\
            .query(
                user_daily_task.ROWID, 
                user.FIRSTNAME,
                user.LASTNAME, 
                exercise.NAME,
                task.QUANTITY,
                daily_task.DATE,
                unit.NAME.label('UNIT'),
                user_daily_task.LINK,
                user_daily_task.COMMENT,
                user_daily_task.MARK
            )\
            .select_from(user_daily_task)\
            .join(daily_task, daily_task.ROWID == user_daily_task.DAILY_TASK)\
            .join(user, user.ROWID == daily_task.AUTHOR)\
            .join(task, task.ROWID == daily_task.TASK)\
            .join(exercise, exercise.ROWID == task.EXERCISE)\
            .join(unit, unit.ROWID == task.UNIT)\
            .where(user_daily_task.USER == id)\
            .order_by(desc(daily_task.DATE))\
            .all()
        return response

    def auth(self, login, password):
        credential = self.tables['credential']
        user = self.tables['user']

        response = self.session\
            .query(credential.USER)\
            .select_from(credential)\
            .join(user, user.ROWID == credential.USER)\
            .where(
                user.EMAIL == login,
                credential.PASSWORD == password,
                )\
            .first()
        return response


    def user_specific(self, id):
        user = self.tables['user']

        response = self.session\
            .query(user)\
            .select_from(user)\
            .where(user.ROWID == id)\
            .first()
        return response


    def user_role_status(self, id, target_role):
        role = self.tables['role']
        user_role = self.tables['user_role']

        response = self.session\
            .query(user_role.STATUS)\
            .select_from(user_role)\
            .join(role, role.ROWID == user_role.ROLE)\
            .where(
                role.NAME == target_role,
                user_role.USER == id
                )\
            .order_by(desc(user_role.TIMESTAMP))\
            .first()

        if response:
            return response[0]
        else:
            return 0
        

    def all_users(self):
        user = self.tables['user']

        response = self.session\
            .query(user)\
            .select_from(user)\
            .all()
        return response


    def update_user(self, data):
        user = self.user_specific(data['rowid'])
        user.FIRSTNAME = data['firstname']
        user.LASTNAME = data['lastname']
        user.PHONE = data['phone']
        user.BIRTHDAY = data['birthday']
        user.EMAIL = data['email']
        user.STATUS = data['status']


    def all_units(self):
        unit = self.tables['unit']

        response = self.session\
            .query(unit)\
            .select_from(unit)\
            .all()
        return response


    def all_exercise(self):
        exercise = self.tables['exercise']

        response = self.session\
            .query(exercise)\
            .select_from(exercise)\
            .all()
        return response


    def exercise_specific(self, id):
        exercise = self.tables['exercise']

        response = self.session\
            .query(exercise)\
            .select_from(exercise)\
            .where(exercise.ROWID == id)\
            .first()
        return response
        

    def update_exercise(self, data):
        exercise = self.exercise_specific(data['id'])
        exercise.NAME = data['name']
        exercise.DESCRIPTION = data['description']
        exercise.LINK = data['link']


    def all_tasks(self):
        task = self.tables['task']
        exercise = self.tables['exercise']
        unit = self.tables['unit']

        response = self.session\
            .query(
                task.ROWID,
                task.QUANTITY, 
                task.COMMENT, 
                exercise.NAME.label('EXERCISE_NAME'), 
                unit.NAME.label('UNIT_NAME'),
            )\
            .select_from(task)\
            .join(exercise, exercise.ROWID == task.EXERCISE)\
            .join(unit, unit.ROWID == task.UNIT)\
            .order_by(exercise.NAME, task.QUANTITY)\
            .all()

        return response


    def task_specific(self, id):
        task = self.tables['task']
        exercise = self.tables['exercise']
        unit = self.tables['unit']

        response = self.session\
            .query(
                task
            )\
            .select_from(task)\
            .where(task.ROWID == id)\
            .first()
        return response


    def task_specific_full(self, id):
        task = self.tables['task']
        exercise = self.tables['exercise']
        unit = self.tables['unit']

        response = self.session\
            .query(
                task.ROWID,
                task.EXERCISE,
                task.QUANTITY,
                task.COMMENT,
                task.UNIT,
                exercise.NAME.label('EXERCISE_NAME'),
                unit.NAME.label('UNIT_NAME')
            )\
            .select_from(task)\
            .join(unit, unit.ROWID == task.UNIT)\
            .join(exercise, exercise.ROWID == task.EXERCISE)\
            .where(task.ROWID == id)\
            .first()
        return response

    def update_task(self, data):
        task = self.task_specific(data['id'])
        task.EXERCISE = data['exercise']
        task.QUANTITY = data['quantity']
        task.COMMENT = data['comment']
        task.UNIT = data['unit']



    def all_daily_task(self):
        daily_task = self.tables['daily_task']
        task = self.tables['task']
        user = self.tables['user']
        exercise = self.tables['exercise']
        unit = self.tables['unit']

        response = self.session\
            .query(
                daily_task.ROWID,
                user.FIRSTNAME,
                user.LASTNAME,
                exercise.NAME.label('EXERCISE_NAME'),
                task.QUANTITY,
                task.COMMENT,
                unit.NAME.label('UNIT_NAME'),
                daily_task.DATE
            )\
            .select_from(daily_task)\
            .join(task, daily_task.TASK == task.ROWID)\
            .join(user, daily_task.AUTHOR == user.ROWID)\
            .join(exercise, exercise.ROWID == task.EXERCISE)\
            .join(unit, unit.ROWID == task.UNIT)\
            .order_by(desc(daily_task.DATE), exercise.NAME, task.QUANTITY)\
            .all()
    
        return response



    def daily_task_on_date(self, date):
        daily_task = self.tables['daily_task']

        response = self.session\
            .query(
                daily_task.DATE,
                daily_task.TASK,
                daily_task.ROWID
            )\
            .select_from(daily_task)\
            .where(daily_task.DATE == date)\
            .all()

        return response


    def daily_task_specific(self, id):
        daily_task = self.tables['daily_task']

        response = self.session\
            .query(
                daily_task
            )\
            .select_from(daily_task)\
            .where(daily_task.ROWID == id)\
            .first()

        return response


    def update_daily(self, id):
        daily_task = self.tables['daily_task']

        response = self.session\
            .query(
                daily_task
            )\
            .select_from(daily_task)\
            .where(daily_task.ROWID == id)\
            .first()

        return response

    def daily_task_recognise(self, data):
        daily_task = self.tables['daily_task']

        response = self.session\
            .query(
                daily_task
            )\
            .select_from(daily_task)\
            .where(
                daily_task.TASK == data['task'],
                daily_task.DATE == data['date']
            )\
            .first()

        return response


    def get_settings(self):
        settings = self.tables['settings']

        response = self.session\
            .query(settings)\
            .select_from(settings)\
            .all()
        return response


    def credential_specific(self, url):
        credential = self.tables['credential']

        response = self.session\
            .query(credential)\
            .select_from(credential)\
            .where(credential.URL == url)\
            .first()
        return response

    def credential_update(self, data):
        credential = self.credential_specific(data['url'])
        credential.URL = ''
        credential.PASSWORD = data['password']

        user = self.user_specific(credential.USER)
        user.STATUS = 1


    def daily_task_user(self, dailyid, userid):
        user_daily_task = self.tables['user_daily_task']
        user = self.tables['user']

        response = self.session\
            .query(
                user_daily_task.LINK,
                user_daily_task.COMMENT,
                user_daily_task.MARK,
                user.FIRSTNAME,
                user.LASTNAME
            )\
            .select_from(user_daily_task)\
            .join(user, user.ROWID == user_daily_task.USER)\
            .where(
                user_daily_task.DAILY_TASK == dailyid,
                user_daily_task.USER == userid,
            )\
            .first()
        return response


    def user_daily_task_get(self, dailyid, userid):
        user_daily_task = self.tables['user_daily_task']
        user = self.tables['user']

        response = self.session\
            .query(
                user_daily_task
            )\
            .select_from(user_daily_task)\
            .join(user, user.ROWID == user_daily_task.USER)\
            .where(
                user_daily_task.DAILY_TASK == dailyid,
                user_daily_task.USER == userid,
            )\
            .first()
        return response


    def daily_task_user_update(self, data):
        user_dail_task = self.user_daily_task_get(data['dailyid'], data['userid'])
        user_dail_task.MARK = data['mark']
        user_dail_task.COMMENT = data['comment']


    def user_daily_task_user(self, userid):
        user_daily_task = self.tables['user_daily_task']
        daily_task = self.tables['daily_task']
        task = self.tables['task']
        exercise = self.tables['exercise']
        unit = self.tables['unit']
        user = self.tables['user']

        response = self.session\
            .query(
                user.FIRSTNAME,
                user.LASTNAME,
                exercise.NAME.label('EXERCISE'),
                unit.NAME.label('UNIT'),
                task.QUANTITY,
                daily_task.DATE,
                user_daily_task.LINK,
                user_daily_task.MARK,
                user_daily_task.COMMENT,
                user_daily_task.ROWID,
                user_daily_task.USER.label('USER')
            )\
            .select_from(user_daily_task)\
            .join(daily_task, daily_task.ROWID == user_daily_task.DAILY_TASK)\
            .join(task, task.ROWID == daily_task.TASK)\
            .join(exercise, exercise.ROWID == task.EXERCISE)\
            .join(unit, unit.ROWID == task.UNIT)\
            .join(user, user.ROWID == daily_task.AUTHOR)\
            .where(user_daily_task.USER == userid)\
            .order_by(desc(daily_task.DATE))\
            .all()
        return response

    def user_link_update(self, userid, dailyid, link):
        user_daily_task = self.tables['user_daily_task']
        response = self.session\
            .query(user_daily_task)\
            .select_from(user_daily_task)\
            .where(
                user_daily_task.USER == userid,
                user_daily_task.ROWID == dailyid
                )\
            .first()

        response.LINK = link
        return response

    def user_daily_group(self, dailyid):
        user_daily_task = self.tables['user_daily_task']

        response = self.session\
            .query(user_daily_task.USER)\
            .select_from(user_daily_task)\
            .where(user_daily_task.DAILY_TASK == dailyid)\
            .all()
        return response

    def check_if_user_exist(self, dailyid, userid):
        user_daily_task = self.tables['user_daily_task']

        response = self.session\
            .query(user_daily_task.ROWID)\
            .select_from(user_daily_task)\
            .where(
                user_daily_task.DAILY_TASK == dailyid,
                user_daily_task.USER == userid,
                )\
            .all()
        return response