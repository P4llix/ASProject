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

    def daily_task_specific(self, day):
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

    

