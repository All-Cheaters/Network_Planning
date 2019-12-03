from wtforms.validators import *
from flask_wtf import FlaskForm
from wtforms import Form, StringField, FieldList, FormField, HiddenField, SelectMultipleField, IntegerField
from wtforms.fields.html5 import DateField


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
    last_time = IntegerField('持续时间')

# class MainForm(FlaskForm):
#     items = FieldList(
#         FormField(ItemsForm)
#     )
