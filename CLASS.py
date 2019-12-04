from datetime import datetime, timedelta


class Link:
    def __init__(self):
        self.fromID = 0  # 边起点
        self.toID = 0  # 边终点


class Knot:
    def __init__(self):
        self.ID = 0
        # 节点ID
        self.name = 0
        # 项目名称
        self.last_time = 0
        # 持续时间
        self.earliest_start_time = 0
        # 工作的最早开始时间
        # =本工作的紧前工作的最早结束时间（有多个时取最大值）
        self.earliest_finish_time = 0
        # 工作的最早完成时间
        # =工作的最早开始时间+工作的持续时间
        self.latest_start_time = 0
        # 工作的最迟开始时间
        # =本工作的紧后工作的最迟开始时间（有多个时取最小值）-工作的持续时间
        self.latest_finish_time = 0
        # 工作的最迟完成时间
        # =工作的最迟开始时间+工作的持续时间
        self.free_time_difference = 0
        # 自由时差
        # =紧后工作最早开始时间（有多个时取最小值）-本工作最早完成时间
        self.total_time_difference = 0
        # 总时差=该工作最迟完成时间
        # =该工作最早完成时间/该工作最迟开始时间-该工作最早开始时间
        self.X = 0
        # 节点横坐标
        self.Y = 0
        # 节点纵坐标
        self.is_key = False
        # 是否为关键节点
        self.pre_item = []
        self.suf_item = []

    def serialize_instance(self):  # 序列化为json
        d = {'__classname__': type(self).__name__}
        d.update(vars(self))
        return d


class Graph:
    def __init__(self):
        self.knotList = []
        # 节点列表,每一个元素是Knot类型
        self.pre_knotList = []
        # 每个节点(v)的前驱点列表 (二维列表)
        # pre_knotList每个元素是一个list
        # list中包含v的所有前驱点ID号
        self.suf_knotList = []
        # 每个节点(v)的后继点列表 (二维列表)
        # suf_knotList每个元素是一个list
        # list中包含v的所有后继点ID号
        self.last_time = 0
        # 项目的持续时间
        self.start_date = datetime(2019, 1, 1)
        # 项目的开始时间
        # type:

    def __IDToPos(self, _ID):  # ID转换到pos,返回int
        pos = -1
        for knot in self.knotList:
            pos += 1
            if knot.ID == _ID:
                break  # ID匹配时break
            else:
                continue
        return pos

    # ---------------------------------↓必看↓---------------------------------#
    #                                                                        #
    #                 解释为什么要有pos:                                       #
    #                 pos是Knot在knotList中存储的坐标                          #
    #                 当只知道ID时并不能直接从knotList中读出该ID对应的节点信息    #
    #                 ID转换成pos,再使用knotList[pos]才能读出该节点信息          #
    #                 总结:函数接口()中都用ID,列表下标[]中都用pos                #
    #                 IDToPos()和posToID()就是解决ID与pos不匹配用的             #
    #                                                                         #
    # ---------------------------------↑必看↑---------------------------------#

    def __posToID(self, _pos):  # pos转换到ID,返回int
        knot = self.knotList[_pos]
        return knot.ID

    def __countEarliestStartTime(self, hisID):  # ---------------------计算最早开始---------------------
        # 工作的最早开始时间 = 本工作的紧前工作的最早结束时间（有多个时取最大值）
        hisPos = self.__IDToPos(hisID)
        his_inDegree = self.getInDegree(hisID)
        if his_inDegree == 0:  # 入度为0,则最早开始时间为0
            self.knotList[hisPos].earliest_start_time = 0
            return
        else:
            HisPreKnotList = self.getPreKnotID(hisID)
            EarliestFinishTimeList = []  # 存所有紧前工作的最早结束时间
            for knotID in HisPreKnotList:  # 所有紧前工作的最早结束时间丢进列表里
                knot_earliest_finish_time = self.getEarliestFinishTime(knotID)
                EarliestFinishTimeList.append(knot_earliest_finish_time)
            his_earliest_start_time = max(EarliestFinishTimeList)  # 所有紧前工作的最早完成时间（最大值）
            self.knotList[hisPos].earliest_start_time = his_earliest_start_time

    def __countEarliestFinishTime(self, hisID):  # ---------------------计算最早结束---------------------
        # 工作的最早完成时间 = 工作的最早开始时间 + 工作的持续时间
        hisPos = self.__IDToPos(hisID)
        his_inDegree = self.getInDegree(hisID)
        if his_inDegree == 0:  # 若入度为0,则最早结束时间为 0 + 持续时间
            self.knotList[hisPos].earliest_finish_time \
                = 0 + self.getLastTime(hisID)
            return
        else:
            his_earliest_start_time = self.getEarliestStartTime(hisID)  # 最早开始
            his_last_time = self.getLastTime(hisID)  # 持续时间
            his_earliest_finish_time = his_earliest_start_time + his_last_time  # 最早完成
            self.knotList[hisPos].earliest_finish_time = his_earliest_finish_time

    def __countLatestStartTime(self, hisID, projectDuration):  # ---------------------计算最迟开始---------------------
        # 工作的最迟开始时间=本工作的紧后工作的最迟开始时间（有多个时取最小值）-工作的持续时间
        hisPos = self.__IDToPos(hisID)
        hisOutDegree = self.getOutDegree(hisID)
        if hisOutDegree == 0:  # 若出度为0,则最迟开始时间为 工期 - 持续时间
            self.knotList[hisPos].latest_start_time \
                = projectDuration - self.getLastTime(hisID)
            return
        else:
            hisSufKnotList = self.getSufKnotID(hisID)
            LatestStartTimeList = []  # 存所有紧后工作的最迟开始时间
            for knotID in hisSufKnotList:  # 所有紧后工作的最迟开始时间丢进列表里
                knot_latest_start_time = self.getLatestStartTime(knotID)
                LatestStartTimeList.append(knot_latest_start_time)
            his_latest_start_time = min(LatestStartTimeList) - self.getLastTime(hisID)
            self.knotList[hisPos].latest_start_time = his_latest_start_time

    def __countLatestFinishTime(self, hisID, projectDuration):  # ---------------------计算最迟结束---------------------
        # 工作的最迟完成时间=工作的最迟开始时间+工作的持续时间
        hisPos = self.__IDToPos(hisID)
        hisOutDegree = self.getOutDegree(hisID)
        if hisOutDegree == 0:  # 若出度为0, 则最迟结束时间为工期
            self.knotList[hisPos].latest_finish_time = projectDuration
            return
        else:
            his_latest_start_time = self.getLatestStartTime(hisID)  # 最迟开始
            his_last_time = self.getLastTime(hisID)  # 持续时间
            his_latest_finish_time = his_latest_start_time + his_last_time  # 最迟完成
            self.knotList[hisPos].latest_finish_time = his_latest_finish_time

    def __countFreeTimeDifference(self, hisID):  # ---------------------计算自由时差---------------------
        # 自由时差=紧后工作最早开始时间（有多个时取最小值）-本工作最早完成时间
        hisPos = self.__IDToPos(hisID)
        hisOutDegree = self.getOutDegree(hisID)
        if hisOutDegree == 0:  # 若出度为0,则自由时差为 工期 - 最早完成
            self.knotList[hisPos].free_time_difference = \
                self.getLatestFinishTime(hisID) - self.getEarliestFinishTime(hisID)
        else:
            hisSufKnotList = self.getSufKnotID(hisID)
            EarliestStartTimeList = []  # 存所有紧后工作最早开始时间
            for knotID in hisSufKnotList:  # 所有紧后工作最早开始时间丢进列表
                earliest_start_time = self.getEarliestStartTime(knotID)
                EarliestStartTimeList.append(earliest_start_time)
            his_free_time_difference = \
                min(EarliestStartTimeList) - self.getEarliestFinishTime(hisID)
            self.knotList[hisPos].free_time_difference = his_free_time_difference

    def __countTotalTimeDifference(self, hisID):  # ---------------------计算总时差---------------------
        # 总时差=该工作最迟完成时间-该工作最早完成时间
        # or 该工作最迟开始时间-该工作最早开始时间
        hisPos = self.__IDToPos(hisID)
        self.knotList[hisPos].total_time_difference = \
            self.getLatestStartTime(hisID) - self.getEarliestStartTime(hisID)
        if self.knotList[hisPos].total_time_difference == 0:
            self.knotList[hisPos].is_key = True

    def __count(self):  # 由拓扑结构和lastTime计算每个节点的其余数值
        topologicalList = self.getTopologicalSorting()
        if topologicalList is None:
            print('有环图')
            return
        else:
            # 最早系列:
            for knotID in topologicalList:
                self.__countEarliestStartTime(knotID)  # 必须先算最早开始再算最早结束
                self.__countEarliestFinishTime(knotID)
            for pos in range(self.getKnotNum()):
                if self.getEarliestFinishTime(self.__posToID(pos)) > self.last_time:
                    self.last_time = self.getEarliestFinishTime(self.__posToID(pos))
            topologicalList.reverse()  # 拓扑序列反转
            # 最晚系列
            for knotID in topologicalList:
                self.__countLatestStartTime(knotID, self.last_time)  # 必须先算最迟开始再算最迟结束
                self.__countLatestFinishTime(knotID, self.last_time)
            # 时差系列
            for knotID in topologicalList:
                self.__countFreeTimeDifference(knotID)
                self.__countTotalTimeDifference(knotID)
        self.__convertToDate()

    def __convertToDate(self):
        for pos in range(self.getKnotNum()):
            self.knotList[pos].earliest_start_time = self.start_date + timedelta(
                days=self.knotList[pos].earliest_start_time)
            self.knotList[pos].earliest_finish_time = self.start_date + timedelta(
                days=self.knotList[pos].earliest_finish_time)
            self.knotList[pos].latest_start_time = self.start_date + timedelta(
                days=self.knotList[pos].latest_start_time)
            self.knotList[pos].latest_finish_time = self.start_date + timedelta(
                days=self.knotList[pos].latest_finish_time)

    def calculateCoordinates(self, canvasSize):
        knotsGroupByXCoord = []  # 将点按横坐标分类，横坐标相同的点构成一个list
        inDegreeList = []  # 初始化入度列表
        zeroInDegreeNum = 0
        knotNum = self.getKnotNum()
        for pos in range(knotNum):
            ID = self.__posToID(pos)
            inDegree = self.getInDegree(ID)
            inDegreeList.append(inDegree)
        while zeroInDegreeNum < knotNum:
            changed = False
            pos = -1
            knotsWithSameXCoord = []  # 储存横坐标相同的点
            for inDegree in inDegreeList:
                pos += 1
                if inDegree == 0:
                    inDegreeList[pos] = -1
                    ID = self.__posToID(pos)
                    knotsWithSameXCoord.append(ID)
                    zeroInDegreeNum += 1
                    changed = True
            knotsGroupByXCoord.append(knotsWithSameXCoord)
            for knotID in knotsWithSameXCoord:
                knotPos = self.__IDToPos(knotID)
                for sufKnotID in self.suf_knotList[knotPos]:
                    sufKnotPos = self.__IDToPos(sufKnotID)
                    inDegreeList[sufKnotPos] -= 1
            if not changed:
                raise TypeError('This graph contains a circle.')
        colsNum = len(knotsGroupByXCoord)
        maxColLength = max(len(col) for col in knotsGroupByXCoord)
        unitXLength = canvasSize[0] // (colsNum + 1)
        unitYLength = canvasSize[1] // (maxColLength + 1)
        for cols in range(colsNum):
            yCoord = (maxColLength - len(knotsGroupByXCoord[cols]) - 1) * unitYLength
            for ID in knotsGroupByXCoord[cols]:
                xCoord = (cols + 1) * unitXLength
                yCoord += 2 * unitYLength
                self.knotList[self.__IDToPos(ID)].X = xCoord
                self.knotList[self.__IDToPos(ID)].Y = yCoord

    def getInDegree(self, knotID):  # 获得某节点的入度,返回int
        """
        :param knotID: 节点ID
        :return: 该ID对应的节点入度
        """
        knotPos = self.__IDToPos(knotID)
        inDegree = len(self.pre_knotList[knotPos])
        return inDegree

    def getOutDegree(self, knotID):  # 获得某节点的出度,返回int
        """
        :param knotID: 节点ID
        :return: 该ID对应的节点入度
        """
        knotPos = self.__IDToPos(knotID)
        outDegree = len(self.suf_knotList[knotPos])
        return outDegree

    def getKnotNum(self):  # 返回节点数量,返回int
        """
        :return:
        """
        return len(self.knotList)

    def getLastTime(self, hisID):  # 获得持续时间,返回int
        hisPos = self.__IDToPos(hisID)
        knot = self.knotList[hisPos]
        return knot.last_time

    def getEarliestStartTime(self, hisID):  # 获得最早开始时间,返回int
        hisPos = self.__IDToPos(hisID)
        knot = self.knotList[hisPos]
        return knot.earliest_start_time

    def getEarliestFinishTime(self, hisID):  # 获得最早完成时间,返回int
        hisPos = self.__IDToPos(hisID)
        knot = self.knotList[hisPos]
        return knot.earliest_finish_time

    def getLatestStartTime(self, hisID):  # 获得最迟开始时间,返回int
        hisPos = self.__IDToPos(hisID)
        knot = self.knotList[hisPos]
        return knot.latest_start_time

    def getLatestFinishTime(self, hisID):  # 获得最迟完成时间,返回int
        hisPos = self.__IDToPos(hisID)
        knot = self.knotList[hisPos]
        return knot.latest_finish_time

    def getKey(self, hisID):
        hisPos = self.__IDToPos(hisID)
        knot = self.knotList[hisPos]
        return knot.is_key

    def getName(self, hisID):
        hisPos = self.__IDToPos(hisID)
        knot = self.knotList[hisPos]
        return knot.name

    def getTopologicalSorting(self):  # 拓扑排序,返回排序后列表, 若为有环图则返回None
        outPutList = []  # 输出的ID
        inDegreeList = []
        zeroInDegreeKnotNum = 0  # 入度为0节点的个数
        knotNum = self.getKnotNum()
        for pos in range(knotNum):  # inDegreeList入度列表初始化成各节点的入度
            ID = self.__posToID(pos)
            inDegree = self.getInDegree(ID)
            inDegreeList.append(inDegree)
        while zeroInDegreeKnotNum < knotNum:  # 当零度节点小于总节点数
            changed = False  # 一次循环下来零度节点数是否有变
            pos = -1  # 每次都要从inDegreeList[0]开始
            for inDegree in inDegreeList:
                pos += 1
                if inDegree == 0:  # 若入度为0
                    inDegreeList[pos] = -1  # 入度从0变成-1,表示该点已过入列表了
                    ID = self.__posToID(pos)  # 入度为0的节点的id号
                    outPutList.append(ID)  # 入度为0时候入列表
                    zeroInDegreeKnotNum += 1  # 零度节点数+1
                    changed = True
                    for knotID in self.suf_knotList[pos]:  # 入栈之后所有以该点为前驱的点入度 -1
                        knotPos = self.__IDToPos(knotID)
                        inDegreeList[knotPos] -= 1
                else:
                    continue
            if not changed:  # 一次循环下来若零度节点数未变,说明有环出现
                return None
        return outPutList

    def inputData(self):  # 输入数据
        print("------↓输入节点↓------退出:q--------\n")  # 点集
        iterID = 0  # 自动生成的ID
        while 1:
            iterID += 1  # 自增
            print('ID = {}'.format(iterID))
            _name = str(input('输入name:\t'))
            if _name == 'q':  # q退出
                break
            _lastTime = int(input('输入lastTime:\t'))
            knot = Knot()  # 实例化一个节点
            knot.ID = iterID  # ID赋值
            knot.name = _name  # name赋值
            knot.last_time = _lastTime  # lastTime赋值
            self.knotList.append(knot)  # 加入点集
        print('\n------↓输入边↓------退出:0--------\n')  # 边集
        knotNum = len(self.knotList)
        for i in range(knotNum):
            self.pre_knotList.append([])
            self.suf_knotList.append([])
        while 1:
            _fromID = int(input('输入前驱ID:'))
            if _fromID == 0:  # 0退出
                break
            _toID = int(input('输入后继ID:'))
            print()
            # 缺输入检查
            link = Link()  # 边实例化
            link.fromID = _fromID  # 前驱点ID
            link.toID = _toID  # 后继点ID
            _fromPos = self.__IDToPos(_fromID)  # 前驱点在knotList中的pos
            _toPos = self.__IDToPos(_toID)  # 后继点在knotList中的pos
            self.pre_knotList[_toPos].append(_fromID)
            self.suf_knotList[_fromPos].append(_toID)

    def info(self):  # 展示数据
        print('-------------数据-------------\n')
        knotNum = len(self.knotList)  # 节点数
        for knotPos in range(knotNum):
            knot = self.knotList[knotPos]
            preKnots = self.getPreKnotID(knot.ID)  # 前驱点
            sufKnots = self.getSufKnotID(knot.ID)  # 后继点
            print("点:({},{})".format(knot.ID, knot.name))  # 节点数据
            print("前驱ID:\t", end='')
            for preKnotID in preKnots:
                print(preKnotID, end='\t')  # print所有前驱点
            print("\n后继ID:\t", end='')
            for sufKnotID in sufKnots:
                print(sufKnotID, end='\t')  # print所有后继点
            print('\n')
        print('-------------具体信息-------------\n')
        for knot in self.knotList:
            print("ID:{}\tname:{}\t总时差:{}"
                  .format(knot.ID, knot.name, knot.total_time_difference))
            print("最早开始:{}\t持续时间:{}\t最早结束:{}"
                  .format(knot.earliest_start_time, knot.last_time, knot.earliest_finish_time))
            print("最迟开始:{}\t自由时差:{}\t最迟结束:{}"
                  .format(knot.latest_start_time, knot.free_time_difference, knot.latest_finish_time))
            print('横坐标:{}\t纵坐标:{}\t是否为关键事件:{}'.format(knot.X, knot.Y, knot.is_key))
            print('\n')

    def readDataFromSQL(self, SQLData, startDate):  # 在数据库中读取数
        # 预计格式
        # {'ID': 1 , 'LT' : 5 , 'name' : superSon , 'pre' : [1,2,3,4] }
        self.last_time = 0
        self.start_date = startDate
        initLinkList = []
        for item in SQLData:
            knot = Knot()
            knot.ID = item['ID']
            knot.last_time = item['LT']
            knot.name = item['name']
            self.knotList.append(knot)
            if item['pre'] == [0]:
                self.pre_knotList.append([])
            else:
                self.pre_knotList.append(item['pre'])
            self.suf_knotList.append([])
            for preKnotID in item['pre']:
                if item['pre'] == [0]:
                    continue
                else:
                    link = Link()
                    link.fromID = preKnotID
                    link.toID = knot.ID
                    initLinkList.append(link)
        for link in initLinkList:
            fromID = link.fromID
            fromPos = self.__IDToPos(fromID)
            toID = link.toID
            self.suf_knotList[fromPos].append(toID)
        for pos in range(len(self.knotList)):
            for ID in self.pre_knotList[pos]:
                name = self.getName(ID)
                self.knotList[pos].pre_item.append(name)
            for ID in self.suf_knotList[pos]:
                name = self.getName(ID)
                self.knotList[pos].suf_item.append(name)
            if len(self.knotList[pos].pre_item) == 0:
                self.knotList[pos].pre_item.append('无')
            if len(self.knotList[pos].suf_item) == 0:
                self.knotList[pos].suf_item.append('无')
        self.__count()

    def getAllRelatedKnotID(self, _ID):  # 获得所有相邻点ID,返回列表
        _pos = self.__IDToPos(_ID)
        related_knotsID = self.pre_knotList[_pos] + self.suf_knotList[_pos]
        return related_knotsID

    def getPreKnotID(self, _ID):  # 获得所有前驱点ID,返回列表
        _pos = self.__IDToPos(_ID)
        return self.pre_knotList[_pos]

    def getSufKnotID(self, _ID):  # 获得所有后继点ID,返回列表
        _pos = self.__IDToPos(_ID)
        return self.suf_knotList[_pos]

    def getCoordinates(self, __ID):
        _pos = self.__IDToPos(__ID)
        knot = self.knotList[_pos]
        return knot.X, knot.Y


class Project:  # 一个工程
    def __init__(self):
        self.graph = Graph()  # 一个工程的进度图
        self.ID = 0
        self.name = 0
        self.startDate = 0  # 工程的开始时间
        self.finishDate = 0  # 工程的结束时间
        self.duration = 0  # 工程工期

    def readDataFromSQL(self, SQLData):
        self.ID = SQLData[0]['ID']
        self.name = SQLData[0]['name']
        self.startDate = datetime.strptime(SQLData[0]['startTime'], "%Y-%m-%d")
        self.finishDate = datetime.strptime(SQLData[0]['finishTime'], "%Y-%m-%d")
        self.duration = int((self.finishDate - self.startDate).days)
        self.graph.readDataFromSQL(SQLData[1], self.startDate)
