from modules import db


class BaseTable(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, unique=True, index=True, nullable=False, autoincrement=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


