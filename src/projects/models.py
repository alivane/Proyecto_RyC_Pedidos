from projects import db, bcrypt


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)
        self.password = self.generate_password_hash(**kwargs)
    
    def generate_password_hash(self, **kwargs):
        if 'password' in kwargs:
            return bcrypt.generate_password_hash(kwargs['password']).decode()

        return None
        