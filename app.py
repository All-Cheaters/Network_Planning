from CLASS import *
from DBconfig import *
from ItemForm import ProjectForm, LoginForm, RegisterForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm(request.form)
    if request.method == 'POST' and loginform.validate_on_submit():
        user_name = loginform.user_name.data
        user_password = loginform.user_password.data
        print(user_name)
        print(user_password)
        user = DBUser.query.filter_by(user_name=user_name).first()
        if user is None:
            flash('用户未注册！')
            return redirect(url_for('register'))
        else:
            if not user.check_password(user_password):
                flash('用户名或密码错误！')
                return redirect(url_for('login'))
            else:
                login_user(user, remember=loginform.remember_me.data)
                print(current_user.get_id())
                return redirect(url_for('new'))
    return render_template('login.html', title='登录', loginform=loginform)


@app.route('/register', methods=['GET', 'POST'])
def register():
    registerform = RegisterForm(request.form)
    if request.method == 'POST' and registerform.validate_on_submit():
        user_name = registerform.user_name.data
        user_password = registerform.user_password.data
        user = DBUser(user_name=user_name,
                      user_password=user_password)
        db.session.add(user)
        try:
            db.session.commit()
            print('注册信息成功提交')
        except Exception as e:
            db.session.rollback()
            print('注册信息提交失败')
            print(e)
        flash('注册成功!')
        return redirect(url_for('new'))
    return render_template('register.html', title='注册', registerform=registerform)


@app.route('/new/', methods=['GET', 'POST'])
@login_required
def new():
    print('--------------------new--------------------')
    form_one = ProjectForm()
    if request.method == 'GET':
        print('GET')
        return render_template('new.html', title='new', form_one=form_one)
    if request.method == 'POST':
        if not form_one.validate_on_submit():
            return render_template('new.html', title='new', form_one=form_one)
        else:
            tempSQLData = [[], []]
            tempProject = {'ID': DBProject.query.count(),
                           'name': form_one.project_name.data,
                           'startTime': form_one.project_ST.data.strftime('%Y-%m-%d'),
                           'finishTime': form_one.project_FT.data.strftime('%Y-%m-%d')}
            tempSQLData[0].append(tempProject)

            form_two = request.form.to_dict(flat=False)
            print(form_two)
            item_key_list = list(form_two.keys())[3:]
            item_value_list = list(form_two.values())[3:]
            print(item_key_list)
            print(item_value_list)
            i = 0
            j = int(str(item_key_list[-1]).split('-')[1])
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
            p = Project()
            tempSQLData = TranslateTempSQLData(tempSQLData)
            isCircle = p.readDataFromSQL(tempSQLData)
            overDue = p.duartion_OK()
            p.graph.calculateCoordinates([1480, 400])
            p.graph.info()
            print(overDue)
            if overDue is False:
                return render_template('new.html', title='new', form_one=form_one, overDue=overDue)
            if isCircle is True:
                return render_template('new.html', title='new', form_one=form_one, isCircle=isCircle)
            else:
                # project数据库对象存储
                db_project = DBProject(project_name=form_one.project_name.data,
                                       project_ST=form_one.project_ST.data,
                                       project_FT=form_one.project_FT.data,
                                       user=current_user.get_id())
                print(db_project)
                db.session.add(db_project)
                # item数据库对象存储
                for Knot in p.graph.knotList:
                    pre_item = ''
                    suf_item = ''
                    for pre in Knot.pre_item:
                        pre_item += pre
                        pre_item += ','
                    for suf in Knot.suf_item:
                        suf_item += suf
                        suf_item += ','
                    db_item = DBItem(item_name=Knot.name,
                                     item_pre_item=pre_item[:-1],
                                     item_suf_item=suf_item[:-1],
                                     item_last_time=Knot.last_time,
                                     item_earliest_start_time=Knot.earliest_start_time.strftime('%Y-%m-%d'),
                                     item_earliest_finish_time=Knot.earliest_finish_time.strftime('%Y-%m-%d'),
                                     item_latest_start_time=Knot.latest_start_time.strftime('%Y-%m-%d'),
                                     item_latest_finish_time=Knot.latest_finish_time.strftime('%Y-%m-%d'),
                                     item_free_time_difference=Knot.free_time_difference,
                                     item_total_time_difference=Knot.total_time_difference,
                                     item_X=Knot.X,
                                     item_Y=Knot.Y,
                                     item_is_key=Knot.is_key,
                                     item_toPoID=Knot.toPoID,
                                     project=DBProject.query.count())
                    print(db_item)
                    db.session.add(db_item)
                try:
                    db.session.commit()
                    print('new表单成功提交')
                except Exception as e:
                    db.session.rollback()
                    print('new表单提交失败')
                    print(e)
                print('project.html')
                return redirect(url_for('project'))


@app.route('/project')
@login_required
def project():
    return render_template('project.html', title='View_AllProject')


@app.route('/view/', methods=['GET', 'POST'])
@login_required
def view():
    projectInfo = ProjectForm()
    print('查看的project_id')
    print(request.args.get('project_id'))
    project = DBProject.query.filter_by(project_id=request.args.get('project_id')).first()
    projectInfo.project_id = project.project_id
    projectInfo.project_name = project.project_name
    projectInfo.project_ST = datetime.datetime.strptime(project.project_ST, '%Y-%m-%d')
    projectInfo.project_FT = datetime.datetime.strptime(project.project_FT, '%Y-%m-%d')
    return render_template('view.html', title='view', projectInfo=projectInfo)


@app.route('/change/', methods=['GET', 'POST'])
@login_required
def change():
    print('--------------------change--------------------')
    if request.method == 'GET':
        project = DBProject.query.filter_by(project_id=request.args.get('project_id')).first()
        project_data = {
            'project_id': project.project_id,
            'project_name': project.project_name,
            'project_ST': datetime.datetime.strptime(project.project_ST, '%Y-%m-%d'),
            'project_FT': datetime.datetime.strptime(project.project_FT, '%Y-%m-%d'),
        }
        form_one = ProjectForm(**project_data)
        print('√1')
        return render_template('change.html', project_id=request.args.get('project_id'), title='change',
                               form_one=form_one)
    if request.method == 'POST':
        form_one = ProjectForm()
        if not form_one.validate_on_submit():
            print('√2')
            return render_template('change.html', project_id=request.args.get('project_id'), title='change',
                                   form_one=form_one)
        else:
            tempSQLData = [[], []]
            tempProject = {'ID': 0, 'name': 0, 'startTime': 0, 'finishTime': 0}
            form_one = ProjectForm()

            # project数据库对象存储
            tempProject['name'] = form_one.project_name.data
            tempProject['startTime'] = form_one.project_ST.data.strftime('%Y-%m-%d')
            tempProject['finishTime'] = form_one.project_FT.data.strftime('%Y-%m-%d')
            tempSQLData[0].append(tempProject)

            # item数据库对象存储
            # 先删除所有project=project_id的Items
            delete_item_list = DBItem.query.filter_by(project=request.args.get('project_id')).all()
            for item in delete_item_list:
                db.session.delete(item)
            form_two = request.form.to_dict(flat=False)
            print(form_two)
            item_key_list = list(form_two.keys())[3:]
            item_value_list = list(form_two.values())[3:]
            # print(item_key_list)
            # print(item_value_list)
            i = 0
            j = int(str(item_key_list[-1]).split('-')[1])
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
            p = Project()
            tempSQLData = TranslateTempSQLData(tempSQLData)
            isCircle = p.readDataFromSQL(tempSQLData)
            overDue = p.duartion_OK()
            p.graph.info()
            print(overDue)
            if overDue is False:
                print('√3')
                return render_template('change.html', project_id=request.args.get('project_id'), title='change',
                                       form_one=form_one, overDue=overDue)
            if isCircle is True:
                print('√4')
                return render_template('change.html', project_id=request.args.get('project_id'), title='change',
                                       form_one=form_one, isCircle=isCircle)
            else:
                # 更新DBProject数据库数据
                DBProject.query.filter_by(project_id=request.args.get('project_id')).update(
                    {"project_name": form_one.project_name.data,
                     "project_ST": form_one.project_ST.data,
                     "project_FT": form_one.project_FT.data})
                for Knot in p.graph.knotList:
                    pre_item = ''
                    suf_item = ''
                    for pre in Knot.pre_item:
                        pre_item += pre
                        pre_item += ','
                    for suf in Knot.suf_item:
                        suf_item += suf
                        suf_item += ','
                    db_item = DBItem(item_name=Knot.name,
                                     item_pre_item=pre_item[:-1],
                                     item_suf_item=suf_item[:-1],
                                     item_last_time=Knot.last_time,
                                     item_earliest_start_time=Knot.earliest_start_time.strftime('%Y-%m-%d'),
                                     item_earliest_finish_time=Knot.earliest_finish_time.strftime('%Y-%m-%d'),
                                     item_latest_start_time=Knot.latest_start_time.strftime('%Y-%m-%d'),
                                     item_latest_finish_time=Knot.latest_finish_time.strftime('%Y-%m-%d'),
                                     item_free_time_difference=Knot.free_time_difference,
                                     item_total_time_difference=Knot.total_time_difference,
                                     item_X=Knot.X,
                                     item_Y=Knot.Y,
                                     item_is_key=Knot.is_key,
                                     item_toPoID=Knot.toPoID,
                                     project=request.args.get('project_id'))
                    print(db_item)
                    db.session.add(db_item)
                try:
                    db.session.commit()
                    print('成功提交')
                except Exception as e:
                    db.session.rollback()
                    print('提交失败')
                    print(e)
                projectInfo = ProjectForm()
                projectInfo.project_id = request.args.get('project_id')
                projectInfo.project_name = form_one.project_name.data
                projectInfo.project_ST = form_one.project_ST.data
                projectInfo.project_FT = form_one.project_FT.data
                print('√5')
                return render_template('view.html', project_id=request.args.get('project_id'), title='view',
                                       projectInfo=projectInfo)


@app.route('/graph/')
@login_required
def graph():
    return render_template('graph.html')


# 获取dbitem的json
@app.route('/getdbitem')
def getbditem():
    print(request.args.get('project_id'))
    view_item_list = DBItem.query.filter_by(project=request.args.get('project_id')).all()
    item_json = []
    for item in view_item_list:
        item_json.append(item.serialize_instance())
    print(item_json)
    return jsonify(item_json)


# 获取pyitem的json
@app.route('/getpyitem')
def getpyitem():
    item_json = []
    for item in DBItem.query.filter().all():
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


@app.route('/deleteproject', methods=['GET', 'POST'])
def deleteproject():
    print('delete内容：')
    print(request.get_json())
    print(request.get_json()['project_id'])
    delete_item_list = DBItem.query.filter_by(project=request.get_json()['project_id']).all()
    for item in delete_item_list:
        db.session.delete(item)
    delete_project = DBProject.query.filter_by(project_id=request.get_json()['project_id']).first()
    print(delete_project)
    db.session.delete(delete_project)
    try:
        db.session.commit()
        print('成功删除')
    except Exception as e:
        db.session.rollback()
        print('删除失败')
        print(e)
    return 'DELETE_OK'


def getIdByName(item_key_list, item_value_list, name):
    index = item_value_list.index([name])
    item_id_key = item_key_list[index]
    item_id = int(item_id_key.split('-')[1]) + 1
    if item_id < 10:
        item_id = '0' + str(item_id)
    return str(item_id)


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
    # db.drop_all()
    # db.create_all()
    app.run(port=5000, debug=True)
