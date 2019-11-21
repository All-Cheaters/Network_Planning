class Link:
    def __init__(self):
        self.fromID = 0  # 边起点
        self.toID = 0  # 边终点


class Knot:
    def __init__(self):
        self.last_time = 0
        # 持续时间
        self.ID = 0
        # 节点ID
        self.name = 0
        # 项目名称
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
        '''
        self.linkList = []
        # 边集列表,每个元素是一个Link (好像也没啥用)
        '''

    def IDToPos(self, _ID):  # ID转换到pos,返回int
        pos = -1
        for knot in self.knotList:
            pos += 1
            if knot.ID == _ID:
                break  # ID匹配时break
            else:
                continue
        return pos

    # ---------------------------------↓必看↓---------------------------------#
    #                 解释为什么要有pos:                                       #
    #                 pos是Knot在knotList中存储的坐标                          #
    #                 当只知道ID时并不能直接从knotList中读出该ID对应的节点信息    #
    #                 ID转换成pos,再使用knotList[pos]才能读出该节点信息          #
    #                 总结:函数接口()中都用ID,列表下标[]中都用pos                #
    # ---------------------------------↑必看↑---------------------------------#

    def posToID(self, _pos):  # pos转换到ID,返回int
        knot = self.knotList[_pos]
        return knot.ID

    def getAllRelatedKnotID(self, _ID):  # 获得所有相邻点ID,返回列表
        _pos = self.IDToPos(_ID)
        related_knotsID = []
        for knotID in self.pre_knotList[_pos]:
            related_knotsID.append(knotID)
        for knotID in self.suf_knotList[_pos]:
            related_knotsID.append(knotID)
        return related_knotsID

    def getPreKnotID(self, _ID):  # 获得所有后继点ID,返回列表
        _pos = self.IDToPos(_ID)
        related_knotsID = []
        for knotID in self.suf_knotList[_pos]:
            related_knotsID.append(knotID)
        return related_knotsID

    def getSufKnotID(self, _ID):  # 获得所有前驱点ID,返回列表
        _pos = self.IDToPos(_ID)
        related_knotsID = []
        for knotID in self.pre_knotList[_pos]:
            related_knotsID.append(knotID)
        return related_knotsID

    def getInDegree(self, knotID):  # 获得某节点的入度,返回int
        inDegree = len(self.getPreKnotID(knotID))
        return inDegree

    def getOutDegree(self, knotID):  # 获得某节点的出度,返回int
        outDegree = len(self.getSufKnotID(knotID))
        return outDegree

    def inputData(self):  # 输入数据
        print("------↓输入节点↓------退出:q--------\n")  # 点集
        iterID = 0  # 自动生成的ID
        while 1:
            iterID += 1  # 自增
            print('ID = {}'.format(iterID))
            _name = str(input('输入name:\t'))
            if _name == 'q':  # q退出
                break
            # _lastTime = int(input('输入lastTime:\t'))
            knot = Knot()  # 实例化一个节点
            knot.ID = iterID  # ID赋值
            knot.name = _name  # name赋值
            # knot.last_time = _lastTime  #lastTtime赋值
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
            _fromPos = self.IDToPos(_fromID)  # 前驱点在knotList中的pos
            _toPos = self.IDToPos(_toID)  # 后继点在knotList中的pos
            self.pre_knotList[_toPos].append(_fromID)
            self.suf_knotList[_fromPos].append(_toID)

    def info(self):  # 展示数据
        print('------数据------\n')
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

    def readDataFromSQL(self):  # 在数据库中读取数
        pass

    def topologicalSorting(self):  # 拓扑排序
        pass

    def count(self):  # 由拓扑结构和lastTime计算每个节点的其余数值
        pass
