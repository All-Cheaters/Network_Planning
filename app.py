from DBconfig import *
from ItemForm import ProjectForm, MainForm


@app.route('/', methods=['GET', 'POST'])
def home():
    return 'HELLO'


@app.route('/try', methods=['GET', 'POST'])
def submit_item():
    form_one = ProjectForm()
    form_two = MainForm()
    if request.method == 'POST':

        # project数据库对象存储
        project_id = 1
        project_name = form_one.project_name.data
        project_ST = form_one.project_ST.data
        project_FT = form_one.project_FT.data
        db_project = DBProject(project_id=project_id,
                               project_name=project_name,
                               project_ST=project_ST,
                               project_FT=project_FT)
        print(db_project)
        db.session.add(db_project)

        # item数据库对象存储
        item_id = 1
        for item in form_two.items.data:
            item_dict = dict(item)  # 每个item是一个dict类型，但是不能用dict的方法，需要先转换成dict类型的变量
            item_keys_list = list(item_dict.keys())  # 字典中的键列表
            item_values_list = list(item_dict.values())  # 字典中的值列表
            print(item_keys_list)
            print(item_values_list)
            item_name = item_values_list[1]

            # item类的前置事件获取
            item_pre_list = item_values_list[2]
            item_pre = ''
            if item_pre_list is not None:
                for pre in item_pre_list:
                    item_pre += pre
                    item_pre += ','
            item_pre = 'null' if (item_pre == '') else item_pre[:-1]

            item_LT = item_values_list[3]
            db_item = DBItem(item_id=item_id,
                             item_name=item_name,
                             item_pre=item_pre,
                             item_LT=item_LT)
            print(db_item)
            item_id += 1
            db.session.add(db_item)

        # 数据库提交
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
    return render_template('try.html', form_one=form_one, form_two=form_two)


@app.route('/view')
def view():
    # #这个函数可以自行修改，以便调试，但是下面四行最好别动
    items = list(DBItem.query.filter().all())
    projects = list(DBProject.query.filter().all())
    print(items)
    print(projects)
    # # 在这里把两个列表传进函数里进行调试操作，比如：
    # # function(items,project)...
    return render_template('view.html', items=items)


if __name__ == '__main__':
    '''
    主函数使用说明：
    1、先直接运行建表
    2、建过表以后把前两句注释，然后将最后一句反注释再运行，这样就不用重复输入数据了
    数据库的数据格式在DBconfig文件里
    '''

    # 在创建数据库表单之前要先删除表单
    db.drop_all()
    # 创建数据库表单
    db.create_all()

    # # 通过view()函数在控制台打印数据库数据，不用管报错，这是最后一行往前端传数据的错，回头再解决
    # view()
    app.run(port=5000, debug=True)
