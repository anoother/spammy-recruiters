from webapp import app, db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import func
from sqlalchemy.orm import validates

# auto-generated index names use the ix_table_column naming convention

class SpamsubMixin(object):
    """
    Provides some common attributes to our models
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __mapper_args__ = {'always_refresh': True}
    id = db.Column(db.Integer, primary_key=True)


class Address(db.Model, SpamsubMixin):
    """
    Address table
    """
    address = db.Column(
        db.String(250),
        nullable=False,
        unique=True,
        index=True)
    timestamp = db.Column(
        db.TIMESTAMP,
        nullable=False,
        default=func.now())

    def __init__(self, address):
        self.address = address

    @classmethod
    def exists(self, address):
        if self.query.filter_by(address=address).first():
            return True
        return False


class Counter(db.Model, SpamsubMixin):
    """
    Counter table
    """
    count = db.Column(
        db.Integer(),
        nullable=False,
        unique=True,
        index=True)
    timestamp = db.Column(
        db.TIMESTAMP,
        nullable=False,
        default=func.now())

    def __init__(self, count):
        self.count = count

    @validates('count')
    def validate_count(self, key, count):
        try:
            assert count >= 0
        except AssertionError:
            count = 0
        return count

class UpdateCheck(db.Model, SpamsubMixin):
    """ Update check timestamp """
    timestamp = db.Column(
        db.TIMESTAMP,
        nullable=False,
        default=func.now())

    def __init__(self):
        self.timestamp = func.now()
