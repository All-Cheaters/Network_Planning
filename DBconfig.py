from flask import *
from flask_sqlalchemy import *
from flask_login import current_user, login_user, logout_user, LoginManager, UserMixin, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test1.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'all_cheaters'

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'  # 登录后查看


@login.user_loader
def load_user(id):
    return DBUser.query.filter_by(user_id=int(id)).first()


class DBUser(UserMixin, db.Model):
    __tablename__ = 'DBUser'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True)
    user_password = db.Column(db.String(20))
    # 对Project为主表，在User里可以用projects查到关联的所有DBProjects
    projects = db.relationship('DBProject', backref='DBUser', lazy='dynamic')

    def get_id(self):
        return self.user_id

    def check_password(self, password):
        return self.user_password == password

    def __repr__(self):
        return {'user_id': self.user_id,
                'user_name': self.user_name,
                'user_password': self.user_password,
                'projects': self.projects}

    def serialize_instance(self):
        d = {'__classname__': type(self).__name__}
        d.update(vars(self))
        d.pop('_sa_instance_state')
        return d


class DBProject(db.Model):
    __tablename__ = 'DBProject'
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(40), unique=True)
    project_ST = db.Column(db.String(10))  # 项目开始时间
    project_FT = db.Column(db.String(10))  # 项目结束时间
    # 对User为子表，在DBProject里可以用user查到User
    # ForeignKey一定要设为DBUser.user_id，而不是user.user_id，因为已经自定义了表名
    user = db.Column(db.Integer, db.ForeignKey('DBUser.user_id'), nullable=False)
    # 对Item为主表，在DBProject里可以用items查到关联的所有DBItems
    # backref一定要设为DBProject
    items = db.relationship('DBItem', backref='DBProject', lazy='dynamic')

    def __repr__(self):
        return str({'ID': self.project_id,
                    'name': self.project_name,
                    'startTime': self.project_ST,
                    'finishTime': self.project_FT,
                    'user': self.user,
                    'items': self.items})

    def serialize_instance(self):
        d = {'__classname__': type(self).__name__}
        d.update(vars(self))
        d.pop('_sa_instance_state')
        return d


class DBItem(db.Model):
    __tablename__ = 'DBItem'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(40))
    item_pre_item = db.Column(db.Text, default='null')  # 前驱事件，在数据库中以逗号分隔id的String类型存储
    item_suf_item = db.Column(db.Text, default='null')  # 后置事件，在数据库中以逗号分隔id的String类型存储
    item_last_time = db.Column(db.Integer)  # 持续时间
    item_earliest_start_time = db.Column(db.String(15))  # 工作的最早开始时间
    item_earliest_finish_time = db.Column(db.String(15))  # 工作的最早完成时间
    item_latest_start_time = db.Column(db.String(15))  # 工作的最迟开始时间
    item_latest_finish_time = db.Column(db.String(15))  # 工作的最迟完成时间
    item_free_time_difference = db.Column(db.Integer)  # 自由时差
    item_total_time_difference = db.Column(db.Integer)  # 总时差
    item_X = db.Column(db.Integer)  # 节点横坐标
    item_Y = db.Column(db.Integer)  # 节点纵坐标
    item_is_key = db.Column(db.Boolean)  # 是否为关键节点，映射到数据库中的是tinyint类型
    item_toPoID = db.Column(db.Integer)  # 拓扑排序的id
    # 对Project为子表，在DBItem里可以用project查到DBProject
    project = db.Column(db.Integer, db.ForeignKey('DBProject.project_id'), nullable=False)

    def __repr__(self):
        return str({'ID': self.item_id,
                    'name': self.item_name,
                    'pre_item': self.item_pre_item,
                    'suf_item': self.item_suf_item,
                    'last_time': self.item_last_time,
                    'earliest_start_time': self.item_earliest_start_time,
                    'earliest_finish_time': self.item_earliest_finish_time,
                    'latest_start_time': self.item_last_time,
                    'latest_finish_time': self.item_latest_finish_time,
                    'free_time_difference': self.item_free_time_difference,
                    'total_time_difference': self.item_total_time_difference,
                    'X': self.item_X,
                    'Y': self.item_Y,
                    'is_key': self.item_is_key,
                    'toPoID': self.item_toPoID,
                    'project': self.project})

    def serialize_instance(self):
        d = {'__classname__': type(self).__name__}
        d.update(vars(self))
        d.pop('_sa_instance_state')
        return d
