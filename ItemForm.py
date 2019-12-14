from wtforms.validators import *
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, BooleanField, PasswordField, SubmitField
from wtforms.fields.html5 import DateField
from DBconfig import DBUser, DBProject
import datetime


# class LateThan(object):
#     def __init__(self, fieldname, message=None):
#         self.fieldname = fieldname
#         self.message = message
#
#     def __call__(self, form, field):
#         try:
#             other = form[self.fieldname]
#         except KeyError:
#             raise ValidationError(field.gettext(u'项目开始时间要小于项目截至时间哦，请重新输入'))
#         # if field.data != other.data:  # --> Change to >= from !=
#         if field.data <= other.data:
#             d = {'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
#                  'other_name': self.fieldname}
#             message = self.message
#             if message is None:
#                 message = field.gettext(u'项目开始时间要小于项目截至时间哦，请重新输入')
#             raise ValidationError(message % d)


class CheckPassword(object):
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
            print(other.data)
        except KeyError:
            raise ValidationError(field.gettext(u'用户名或密码错误！'))
        # if field.data != other.data:  # --> Change to >= from !=
        user = DBUser.query.filter_by(user_name=other.data).first()
        if user is None or user.user_password != field.data:
            d = {'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                 'other_name': self.fieldname}
            message = self.message
            if message is None:
                message = field.gettext(u'用户名或密码错误！')
            raise ValidationError(message % d)


class CheckProjectName(object):
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
            print(other.data)
        except KeyError:
            raise ValidationError(field.gettext(u'不能修改项目名哦!'))
        # if field.data != other.data:  # --> Change to >= from !=
        if str(other.data) == 'None':
            project = DBProject.query.filter_by(project_name=field.data).first()
            if project is not None:
                d = {'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                     'other_name': self.fieldname}
                message = self.message
                if message is None:
                    message = field.gettext(u'项目名重复了，请您换一个吧!')
                raise ValidationError(message % d)
        else:
            project = DBProject.query.filter_by(project_id=other.data).first()
            if field.data != project.project_name:
                d = {'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                     'other_name': self.fieldname}
                message = self.message
                if message is None:
                    message = field.gettext(u'不能修改项目名哦!')
                raise ValidationError(message % d)


class ProjectForm(FlaskForm):
    project_id = HiddenField(u'项目ID')
    project_name = StringField(u'项目名称', validators=[CheckProjectName('project_id')], render_kw={"placeholder": "项目名称"})
    project_ST = DateField(u'起始时间', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"placeholder": "开始时间"})
    project_FT = DateField(u'截止时间', format='%Y-%m-%d', validators=[DataRequired()],
                           render_kw={"placeholder": "截止时间"})  # , LateThan('project_ST')]

    # def validate_project_name(self, project_name):
    #     project = DBProject.query.filter_by(project_name=project_name.data).first()
    #     if project is not None:
    #         raise ValidationError('项目名重复了，请您换一个吧!')


class LoginForm(FlaskForm):
    user_name = StringField(u'用户名', validators=[DataRequired(message='请输入用户名')], render_kw={"placeholder": "账号"})
    user_password = PasswordField(u'用户密码', validators=[DataRequired(message='请输入密码'), CheckPassword('user_name')],
                                  render_kw={"placeholder": "密码"})
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')

    def validate_user_name(self, user_name):
        user = DBUser.query.filter_by(user_name=user_name.data).first()
        if user is None:
            raise ValidationError('用户名不存在!')


class RegisterForm(FlaskForm):
    user_name = StringField(u'用户名', validators=[DataRequired(message='请输入用户名')], render_kw={"placeholder": "账号"})
    user_password = PasswordField(u'用户密码', validators=[DataRequired(message='请输入密码')], render_kw={"placeholder": "密码"})
    user_password2 = PasswordField(u'确认密码', validators=[DataRequired(), EqualTo('user_password')],
                                   render_kw={"placeholder": "确认密码"})
    submit = SubmitField(u'注册')

    def validate_user_name(self, user_name):
        user = DBUser.query.filter_by(user_name=user_name.data).first()
        if user is not None:
            raise ValidationError('用户名重复了，请您换一个吧!')
