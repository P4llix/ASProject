class User:
    def __init__(self, db):
        self.db = db
        self.roles = {}
        self.rowid = 0
    
    def set_id(self, id):
        self.id = id

    def set_personal(self):
        personal_info = self.db.user_specific(self.id)
        self.rowid = personal_info.ROWID
        self.firstname = personal_info.FIRSTNAME
        self.lastname = personal_info.LASTNAME
        self.fullname = self.firstname + ' ' + self.lastname
        self.phone = personal_info.PHONE
        self.birthday = personal_info.BIRTHDAY
        self.email = personal_info.EMAIL
        self.status = personal_info.STATUS
        self.comment = personal_info.COMMENT

    def get_roles(self, roles = ['ADMIN', 'MOD', 'USER']):
        for role in roles:
            query = self.db.user_role_status(self.id, role)
            if query:
                self.roles[role] = 1
            else:
                self.roles[role] = 0

    def __str__(self):
        return f'{self.rowid}'
