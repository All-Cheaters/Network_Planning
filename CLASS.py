class Link:
    def __init__(self, ):
        self.fromID = 0  # 边起点
        self.toID = 0  # 边终点


class Knot:
    def __init__(self):
        self.lastTime = 0
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
        self.lastest_start_time = 0
        # 工作的最迟开始时间
        # =本工作的紧后工作的最迟开始时间（有多个时取最小值）-工作的持续时间
        self.lastest_finish_time = 0
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
        self.knotlist = []  # 节点列表
        self.linklist_to = []  # tolink列表
        self.linklist_from = []  # fromlink列表
        self.Mat = []  # 邻接矩阵

    def IDtopos(self, _ID):  # ID转换到pos
        pos = -1
        for knot in self.knotlist:
            pos += 1
            if knot.ID == _ID:
                break  # ID匹配时break
            else:
                continue
        return pos

    def postoID(self, _pos):  # pos转换到ID
        knot = self.knotlist[_pos]
        return knot.ID

    def getAllRelatedKnotID(self, _ID):  # 获得所有相邻点
        _pos = self.IDtopos(_ID)
        related_knots = []
        for link in self.linklist_from[_pos]:
            knotID = link.fromID
            related_knots.append(knotID)
        for link in self, linklist_to[_pos]:
            knotID = link.toID
            related_knots.append(knotID)
        return related_knots

    def getToRelatedKnotID(self, _ID):  # 获得后继点
        _pos = self.IDtopos(_ID)
        related_knots = []
        for link in self.linklist_to[_pos]:
            knotID = link.toID
            related_knots.append(knotID)
        return related_knots

    def getFromRelatedKnotID(self, _ID):  # 获得前驱点
        _pos = self.IDtopos(_ID)
        related_knots = []
        for link in self.linklist_from[_pos]:
            knotID = link.fromID
            related_knots.append(knotID)
        return related_knots

    def inputData(self):  # 输入数据
        print('------↓输入节点↓------退出:q--------\n')  # 点集
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
            # knot.lastTime = _lastTime  #lastTtime赋值
            self.knotlist.append(knot)  # 加入点集
        print('\n------↓输入边↓------退出:0--------\n')  # 边集
        knotnum = len(self.knotlist)
        for i in range(knotnum):
            self.linklist_from.append([])  # 为每一个节点创建一个前驱边集
            self.linklist_to.append([])  # 为每一个节点创建一个后继边集
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
            _frompos = self.IDtopos(_fromID)  # 前驱点在knotlist中的pos
            _topos = self.IDtopos(_toID)  # 后继点在knotlist中的pos
            self.linklist_to[_frompos].append(link)  # 前驱点边集加入link
            self.linklist_from[_topos].append(link)  # 后继点边集加入link

    def info(self):  # 展示数据
        print('------数据------\n')
        knotnum = len(self.knotlist)  # 节点数
        for knotpos in range(knotnum):
            knot = self.knotlist[knotpos]
            preknots = self.getFromRelatedKnotID(knot.ID)  # 前驱点
            backknots = self.getToRelatedKnotID(knot.ID)  # 后继点
            print("点:({},{})".format(knot.ID, knot.name))  # 节点数据
            print("前驱ID:\t", end='')
            for preknotID in preknots:
                print(preknotID, end='\t')  # print所有前驱点
            print("\n后继ID:\t", end='')
            for backknotID in backknots:
                print(backknotID, end='\t')  # print所有后继点
            print('\n')

    def countData(self):
        pass
