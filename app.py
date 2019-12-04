from CLASS import *
from DBconfig import *
from ItemForm import ProjectForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/new/', methods=['GET', 'POST'])
def new():
    form_one = ProjectForm()
    if request.method == 'GET':
        return render_template('new.html', title='new', form_one=form_one)
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
        form_two = request.form.to_dict(flat=False)
        print(form_two)
        item_key_list = list(form_two.keys())[3:]
        item_value_list = list(form_two.values())[3:]
        print(item_key_list)
        print(item_value_list)
        i = 0
        j = int(item_key_list[-1][6])
        while i <= j:
            item_id = i
            item_index = item_key_list.index('items-' + str(i) + '-item_name')
            item_name = item_value_list[item_index][0]
            item_pre = ''
            item_LT = ''
            if item_key_list[item_index + 1] == 'items-' + str(i) + '-item_pre':
                for pre in item_value_list[item_index + 1]:
                    if pre != '0':
                        item_pre = item_pre + getIdByName(item_key_list, item_value_list, pre) + ' ' + pre + ','
                item_pre = '00' if (item_pre == '') else item_pre[:-1]
                item_LT = item_value_list[item_index + 2][0]
            else:
                item_pre = '00'
                item_LT = item_value_list[item_index + 1][0]
            i += 1
            print(item_id + 1)
            print(item_name)
            print(item_pre)
            print(item_LT)
            db_item = DBItem(item_id=item_id + 1,
                             item_name=item_name,
                             item_pre=item_pre,
                             item_LT=item_LT)
            db.session.add(db_item)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)

        # 计算
        SQLData = TranslateToSQLData()
        p.readDataFromSQL(SQLData)
        p.graph.calculateCoordinates([1000, 500])
        p.graph.info()
        return render_template('view.html', title='view')


@app.route('/view/')
def view():
    return render_template('view.html', title='view')


@app.route('/change/', methods=['GET', 'POST'])
def change():
    form_one = ProjectForm()
    if request.method == 'GET':
        for project in DBProject.query.filter().all():
            form_one.project_id = project.project_id
            form_one.project_name = project.project_name
            form_one.project_ST = project.project_ST
            form_one.project_FT = project.project_FT
        return render_template('change.html', title='change', form_one=form_one)
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
        form_two = request.form.to_dict(flat=False)
        print(form_two)
        item_key_list = list(form_two.keys())  # [3:]
        item_value_list = list(form_two.values())  # [3:]
        print(item_key_list)
        print(item_value_list)
        i = 0
        j = int(item_key_list[-1][6])
        while i <= j:
            item_id = i
            item_index = item_key_list.index('items-' + str(i) + '-item_name')
            item_name = item_value_list[item_index][0]
            item_pre = ''
            item_LT = ''
            if item_key_list[item_index + 1] == 'items-' + str(i) + '-item_pre':
                for pre in item_value_list[item_index + 1]:
                    if pre != '0':
                        item_pre = item_pre + getIdByName(item_key_list, item_value_list, pre) + ' ' + pre + ','
                item_pre = '00' if (item_pre == '') else item_pre[:-1]
                item_LT = item_value_list[item_index + 2][0]
            else:
                item_pre = '00'
                item_LT = item_value_list[item_index + 1][0]
            i += 1
            print(item_id + 1)
            print(item_name)
            print(item_pre)
            print(item_LT)
            db_item = DBItem(item_id=item_id + 1,
                             item_name=item_name,
                             item_pre=item_pre,
                             item_LT=item_LT)
            db.session.add(db_item)

        try:
            db.drop_all()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)

        # 计算
        SQLData = TranslateToSQLData()
        p.readDataFromSQL(SQLData)
        p.graph.calculateCoordinates([1000, 500])
        p.graph.info()
        return render_template('view.html', title='view')


@app.route('/graph/')
def graph():
    return render_template('graph.html')


# 获取dbitem的json
@app.route('/getdbitem')
def bditem():
    item_json = []
    for item in DBItem.query.filter().all():
        item_json.append(item.serialize_instance())
    print(item_json)
    return jsonify(item_json)


# 获取pyitem的json
@app.route('/getpyitem')
def pyitem():
    item_json = []
    for item in p.graph.knotList:
        item_json.append(item.serialize_instance())
    print(item_json)
    return jsonify(item_json)


# 获取project的json
@app.route('/getproject')
def getproject():
    project_json = []
    for project in DBProject.query.filter().all():
        project_json.append(project.serialize_instance())
    print(project_json)
    return jsonify(project_json)


def getIdByName(item_key_list, item_value_list, name):
    index = item_value_list.index([name])
    item_id_key = item_key_list[index]
    item_id = int(item_id_key.split('-')[1]) + 1
    if item_id < 10:
        item_id = '0' + str(item_id)
    return item_id


def TranslateToSQLData():  # 只能读一个项目
    projects = DBProject.query.filter().all()
    projectList = []
    projectsDict = {}
    items = DBItem.query.filter().all()
    itemList = []
    for statement in projects:
        projectsDict = eval(str(statement))
        projectList.append(projectsDict)
    for statement in items:
        itemDict = eval(str(statement))
        itemList.append(itemDict)
    for itemPos in range(len(itemList)):
        itemDict = itemList[itemPos]
        IDList = str.split((itemDict['pre']), sep=',')  # 得到的是['01:A','02:B','03:C']
        for pos in range(len(IDList)):
            IDList[pos] = int(IDList[pos][:2])
        itemList[itemPos]['pre'] = IDList
    return projectsDict, itemList


if __name__ == '__main__':
    # 在创建数据库表单之前要先删除表单
    db.drop_all()
    # 创建数据库表单
    db.create_all()
    # 全局变量工程，储存计算节点
    p = Project()
    # SQLData = TranslateToSQLData()
    # p.readDataFromSQL(SQLData)
    # p.graph.calculateCoordinates([1000, 500])
    # p.graph.info()
    # 通过view()函数在控制台打印数据库数据，不用管报错，这是最后一行往前端传数据的错，回头再解决
    # view()
    app.run(port=5000, debug=True)
