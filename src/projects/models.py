from projects import db, bcrypt


class Pedidos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_user = db.Column(db.String, nullable=False)
    rut = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    name_menu = db.Column(db.String, nullable=False)
    terminated = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        super(Pedidos, self).__init__(**kwargs)
