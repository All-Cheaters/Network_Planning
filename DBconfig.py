from flask import *
from flask_sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test1.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'all_cheaters'

db = SQLAlchemy(app)


class DBProject(db.Model):
    __tablename__ = 'Projects'
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(40))
    project_ST = db.Column(db.Integer)  # 项目开始时间
    project_FT = db.Column(db.Integer)  # 项目结束时间

    # DBItems = db.relationship('DBItem', backref='DBProject', lazy=True)

    def __repr__(self):
        return str({'ID': self.project_id,
                    'name': self.project_name,
                    'startTime': self.project_ST,
                    'finishTime': self.project_FT, })

    def serialize_instance(self):
        d = {'__classname__': type(self).__name__}
        d.update(vars(self))
        d.pop('_sa_instance_state')
        return d


class DBItem(db.Model):
    __tablename__ = 'Items'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(40))
    item_pre = db.Column(db.Text, default='null')  # 前驱事件，在数据库中以逗号分隔id的String类型存储
    item_LT = db.Column(db.Integer)  # 持续时间

    # DBProject = db.Column(db.Integer, db.ForeignKey('DBProject.id'), nullable=False)
    def __repr__(self):
        return str({'ID': self.item_id,
                    'name': self.item_name,
                    'pre': self.item_pre,
                    'LT': self.item_LT, })

    def serialize_instance(self):
        d = {'__classname__': type(self).__name__}
        d.update(vars(self))
        d.pop('_sa_instance_state')
        return d


class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return {'user_id': self.user_id,
                'user_name': self.user_name, }

    def serialize_instance(self):
        d = {'__classname__': type(self).__name__}
        d.update(vars(self))
        d.pop('_sa_instance_state')
        return d
