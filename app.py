from CLASS import *
from DBconfig import *
from ItemForm import ProjectForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/new/', methods=['GET', 'POST'])
def new():
    print('--------------------new--------------------')
    form_one = ProjectForm()
    if request.method == 'GET':
        return render_template('new.html', title='new', form_one=form_one)
    if request.method == 'POST':
        tempSQLData = [[], []]
        tempProject = {'ID': 1, 'name': form_one.project_name.data,
                       'startTime': form_one.project_ST.data.strftime('%Y-%m-%d'),
                       'finishTime': form_one.project_FT.data.strftime('%Y-%m-%d')}
        tempSQLData[0].append(tempProject)

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
            item_id = i + 1
            item_index = item_key_list.index('items-' + str(i) + '-item_name')
            item_name = item_value_list[item_index][0]
            item_pre = ''
            item_LT = ''
            if item_key_list[item_index + 1] == 'items-' + str(i) + '-item_pre':
                for pre in item_value_list[item_index + 1]:
                    if pre not in ['0', '无']:
                        item_pre = item_pre + getIdByName(item_key_list, item_value_list, pre) + ' ' + pre + ','
                item_pre = '00' if (item_pre == '') else item_pre[:-1]
                item_LT = item_value_list[item_index + 2][0]
            else:
                item_pre = '00'
                item_LT = item_value_list[item_index + 1][0]
            i += 1
            tempSQLData[1].append({'ID': int(item_id), 'LT': int(item_LT), 'name': item_name, 'pre': item_pre})
        # 计算
        ItemIntoSQLFile = tempSQLData[1].copy()
        tempSQLData = TranslateTempSQLData(tempSQLData)
        isCircle = p.readDataFromSQL(tempSQLData)
        p.graph.calculateCoordinates([1000, 500])
        p.graph.info()
        if isCircle is True:
            return render_template('new.html', title='new', form_one=form_one, isCircle=isCircle)
        else:
            # project数据库对象存储
            # project_id = 1
            project_name = form_one.project_name.data
            project_ST = form_one.project_ST.data
            project_FT = form_one.project_FT.data
            db_project = DBProject(project_name=project_name,  # project_id=project_id,
                                   project_ST=project_ST,
                                   project_FT=project_FT)
            print(db_project)
            db.session.add(db_project)

            for itemDict in ItemIntoSQLFile:
                db_item = DBItem(item_id=itemDict['ID'],
                                 item_name=itemDict['name'],
                                 item_pre=itemDict['pre'],
                                 item_LT=itemDict['LT'])
                print(db_item)
                db.session.add(db_item)
            try:
                db.session.commit()
                print('成功提交')
            except Exception as e:
                db.session.rollback()
                print('提交失败')
                print(e)
            return render_template('view.html', title='view')


@app.route('/view/')
def view():
    return render_template('view.html', title='view')


@app.route('/change/', methods=['GET', 'POST'])
def change():
    print('--------------------change--------------------')
    if request.method == 'GET':
        project_data = {}
        for project in DBProject.query.filter().all():
            project_data = {
                'project_id': project.project_id,
                'project_name': project.project_name,
                'project_ST': datetime.datetime.strptime(project.project_ST, '%Y-%m-%d'),
                'project_FT': datetime.datetime.strptime(project.project_FT, '%Y-%m-%d'),
            }
        form_one = ProjectForm(**project_data)
        return render_template('change.html', title='change', form_one=form_one)
    if request.method == 'POST':
        tempSQLData = [[], []]
        tempProject = {'ID': 0, 'name': 0, 'startTime': 0, 'finishTime': 0}
        form_one = ProjectForm()
        # project数据库对象存储
        project_id = DBProject.query.filter_by(project_name=form_one.project_name.data).first().project_id

        tempProject['ID'] = int(project_id)
        tempProject['name'] = form_one.project_name.data
        tempProject['startTime'] = form_one.project_ST.data.strftime('%Y-%m-%d')
        tempProject['finishTime'] = form_one.project_FT.data.strftime('%Y-%m-%d')
        tempSQLData[0].append(tempProject)

        # item数据库对象存储
        DBItem.query.delete()  # 删除所有行，返回删除的行数
        form_two = request.form.to_dict(flat=False)
        print(form_two)
        item_key_list = list(form_two.keys())[3:]
        item_value_list = list(form_two.values())[3:]
        # print(item_key_list)
        # print(item_value_list)
        i = 0
        j = int(item_key_list[-1][6])
        while i <= j:
            item_id = i + 1
            item_index = item_key_list.index('items-' + str(i) + '-item_name')
            item_name = item_value_list[item_index][0]
            item_pre = ''
            item_LT = ''
            if item_key_list[item_index + 1] == 'items-' + str(i) + '-item_pre':
                for pre in item_value_list[item_index + 1]:
                    if pre not in ['0', '无']:
                        item_pre = item_pre + getIdByName(item_key_list, item_value_list, pre) + ' ' + pre + ','
                item_pre = '00' if (item_pre == '') else item_pre[:-1]
                item_LT = item_value_list[item_index + 2][0]
            else:
                item_pre = '00'
                item_LT = item_value_list[item_index + 1][0]
            i += 1
            tempSQLData[1].append({'ID': int(item_id), 'LT': int(item_LT), 'name': item_name, 'pre': item_pre})

        # 计算
        IntoSQLFile = tempSQLData[1].copy()
        tempSQLData = TranslateTempSQLData(tempSQLData)
        tempP = Project()
        isCircle = tempP.readDataFromSQL(tempSQLData)
        tempP.graph.calculateCoordinates([1000, 500])
        tempP.graph.info()
        if isCircle is True:
            return render_template('change.html', title='change', form_one=form_one, isCircle=isCircle)
        else:
            p.readDataFromSQL(tempSQLData)
            try:
                DBProject.query.filter_by(project_name=form_one.project_name.data).update({"project_id": project_id,
                                                                                           "project_name": form_one.project_name.data,
                                                                                           "project_ST": form_one.project_ST.data,
                                                                                           "project_FT": form_one.project_FT.data})
                for itemDict in IntoSQLFile:
                    db_item = DBItem(item_id=itemDict['ID'],
                                     item_name=itemDict['name'],
                                     item_pre=itemDict['pre'],
                                     item_LT=itemDict['LT'])
                    db.session.add(db_item)
                db.session.commit()
                print('成功提交')
            except Exception as e:
                db.session.rollback()
                print('提交失败')
                print(e)
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


def TranslateTempSQLData(tempSQLData):
    projects = tempSQLData[0]

    projectList = []
    projectsDict = {}
    items = tempSQLData[1]

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


def TranslateToSQLData():  # 只能读一个项目
    projects = DBProject.query.filter().all()
    print('\nIN NEW projects-------------------------')
    print(projects)
    print('projects-------------------------\n')
    projectList = []
    projectsDict = {}
    items = DBItem.query.filter().all()
    print('\nIN NEW items-------------------------')
    print(items)
    print('items-------------------------\n')
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
