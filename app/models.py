from sqlalchemy.orm.exc import NoResultFound

from app import db


class BucketList(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name):
        """initialize with name."""
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return BucketList.query.all()

    @staticmethod
    def fetch_by_id(id):
        try:
            return db.session.query(BucketList).filter(BucketList.id == id).one()
        except NoResultFound:
            print "No rows exists"
            return None

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)

    def __unicode__(self):
        return "<Bucketlist: {} - {}>".format(self.name, self.id)

    def __str__(self):
        return "<Bucketlist: {} - {}>".format(self.id, self.name)


class Task(db.Model):
    """This class represents the tasks table."""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    done = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, title, description):
        """initialize with name."""
        self.title = title
        self.description = description

    def __repr__(self):
        return "<Task id: {}, title: {}, title: {}>".format(self.id, self.title, self.description)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Task.query.all()

    @staticmethod
    def fetch_by_name(name):
        try:
            return db.session.query(Task).filter(Task.name == name).first()
        except NoResultFound:
            print "No rows exists"
            return None

    @staticmethod
    def fetch_by_id(id):
        try:
            return db.session.query(Task).filter(Task.id == id).first()
        except NoResultFound:
            print "No rows exists"
            return None

    def delete(self):
        db.session.delete(self)
        db.session.commit()