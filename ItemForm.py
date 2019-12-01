from wtforms.validators import *
from flask_wtf import FlaskForm
from wtforms import Form, StringField, FieldList, FormField, HiddenField, SelectMultipleField
from wtforms.fields.html5 import DateField


# class ItemForm(FlaskForm):  # FlaskForm继承自Form
#     ID = StringField('id')
#     name = StringField('事项名称', [validators.Length(min=1, max=40)])
#     pre = StringField('前驱', [validators.required()])
#     LT = IntegerField('持续时间')
#     ES = IntegerField('最早开始时间')
#     LS = IntegerField('最晚开始时间')
#     TF = IntegerField('总时差')
#     EF = IntegerField('最早结束时间')
#     LF = IntegerField('最晚结束时间')
#     FF = IntegerField('自由时差')
#     submit = SubmitField('提交')

class ProjectForm(FlaskForm):
    project_id = HiddenField('项目ID')
    project_name = StringField('工程名称')
    project_ST = DateField('起始时间', format='%Y-%m-%d')
    project_FT = DateField('截止时间', format='%Y-%m-%d')


class ItemsForm(Form):
    item_id = HiddenField('事件ID')
    item_name = StringField('事件名称')
    pre_item = SelectMultipleField('前驱事件')
    # 暂定为string类型，加到date的%d里，具体我也不会，实现不了可以再改
    last_time = StringField('持续时间')


class MainForm(FlaskForm):
    items = FieldList(
        FormField(ItemsForm)
    )
