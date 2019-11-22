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
        return str({'project_id': self.project_id,
                    'project_name': self.project_name,
                    'project_ST': self.project_ST,
                    'project_FT': self.project_FT, })


class DBItem(db.Model):
    __tablename__ = 'Items'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(40))
    item_pre = db.Column(db.Text, default='null')  # 前驱事件，在数据库中以逗号分隔id的String类型存储
    item_LT = db.Column(db.Integer)  # 持续时间

    # DBProject = db.Column(db.Integer, db.ForeignKey('DBProject.id'), nullable=False)

    def __repr__(self):
        return str({'item_id': self.item_id,
                    'item_name': self.item_name,
                    'item_ST': self.item_pre,
                    'item_FT': self.item_LT, }
                   )


class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return {'user_id': self.user_id,
                'user_name': self.user_name, }
