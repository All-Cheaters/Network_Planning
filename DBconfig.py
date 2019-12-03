from flask import *
from flask_sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test1.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'all_cheaters'
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)


class DBProject(db.Model):
    __tablename__ = 'Projects'
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(40))
    project_ST = db.Column(db.Integer)  # 项目开始时间
    project_FT = db.Column(db.Integer)  # 项目结束时间
    # DBItems = db.relationship('DBItem', backref='DBProject', lazy=True)

    def __repr__(self):
        return '<Id %s>' % self.project_id \
               + '\n<Name %s>' % self.project_name \
               + '\n<ST %s>' % self.project_ST \
               + '\n<FT %s>' % self.project_FT


class DBItem(db.Model):
    __tablename__ = 'Items'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(40))
    item_pre = db.Column(db.String(20), default=0)  # 前驱事件，在数据库中以逗号分隔id的String类型存储
    item_LT = db.Column(db.Integer)  # 持续时间
    # DBProject = db.Column(db.Integer, db.ForeignKey('DBProject.id'), nullable=False)

    def __repr__(self):
        return '<Id %s>' % self.item_id \
               + '\n<Name %s>' % self.item_name \
               + '\n<pre %s>' % self.item_pre \
               + '\n<LT %s>' % self.item_LT


class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return '<Id %s>' % self.user_id \
               + '<\nName %s>' % self.user_name
