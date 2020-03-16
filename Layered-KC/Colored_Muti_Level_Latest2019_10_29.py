import graphviz as gv
import os
import random
import time

os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'
Gindex = 0  # for the index of requirement node  can't change
TIMES = 40000  # a suitable number, better not bigger than 250000
Failure = 0  # to observe the failure times
RequestIndex = 0  # I only want to record the successful requirement
result = []
PATH = ".\\codeLatest.gv"  # used for the outputfile of the string tree
PATH2 = ".\\requestTreeLatest.gv"  # used for the outputfile of the request tree
MinIncreaseLen = 1  # represent the minimum difference compared with the director predecessor
MaxIncreaseLen = 8  # represent the maximum difference compared with the director predecessor
GlobalSpace = []

'''
NOTE:
the Muti Level program also used the global check we talked about last time.
the outputfile includes the code tree and the request tree.
'''


# represent the Node appear in the output tree.
class Node:
    sself = ''  # the binary string for itself
    space = ''  # the left space for the node(string)
    F = set()  # F set in KC theorem
    preRe = ''
    index = 0
    color = ''
    retrieve = 0

    def __init__(self, s, sp, setF, pre, index, color):
        self.sself = s
        self.space = sp
        self.F = setF
        self.preRe = pre
        self.index = index
        self.color = color
        self.retrieve = 0

    def getString(self):
        return self.sself

    def getSpace(self):
        return self.space

    def getF(self):
        return self.F

    def getPreRe(self):
        return self.preRe

    def getIndex(self):
        return self.index

    def getColor(self):
        return self.color

    def getRetrive(self):
        return self.retrieve

    def UpdateRetrive(self):
        self.retrieve = 1

    def UpdateSpace(self, newSpace):
        self.space = newSpace

    def UpdateF(self, newF):
        self.F = newF

# this function is used to do copy when the left space is not enough.
# this function used for copy to enlarge the space to meet the requirement.
# CopyLen: the required length  selfLoc: the index of yourself in request.
def Copy(CopyLen, selfLoc, grandFather, result, cdot, requestdot):
    # this is the exit of the function
    if grandFather in "*":  # represent the path has reached the root of the tree. represent the root is applying for space, this must be wrong
        return False
    global Gindex
    # if code goes here, means that the level has not reached the root
    ancestor = int(grandFather)  # ancestor represents the index of the first node that has enough space for its child's copy
    ancesorList = result[ancestor]
    start = 0
    copyFlag = 0

    while copyFlag == 0:
        j1 = start
        while j1 < len(ancesorList):  # traverse all the node if necessary, if we can find one which has enough space, then we jus break
            node = ancesorList[j1]
            curSpace = node.getSpace()
            difflen = CopyLen - len(curSpace)

            while difflen > 0:
                difflen -= 1
                curSpace.append(0)
            position = CopyLen - 1
            while position >= 0 and curSpace[position] != 1:
                position -= 1
            if position == -1:  # represent this node hasn't enough space
                j1 += 1
            else:  # represent this node has enough space
                # update the curSpace
                curSpace[position] = 0
                for x in range(position + 1, CopyLen):
                    curSpace[x] = 1
                node.UpdateSpace(curSpace)  # the node update its space

                if not node.getF():  # means node.getF() is empty, cause if node.getF() is empty   node.getF() ===False
                    baseString = node.getString()  # the string of node itself, equally the new string's former part
                    baseLen = len(baseString)
                    zeros = CopyLen - baseLen
                    tmpx = 0
                    tmpStr = []
                    while tmpx < zeros:  # just add some zeros after the node.getString()
                        tmpx += 1
                        tmpStr.append('0')
                    
                    curOutPut = baseString + "".join(tmpStr)
                    tmpF = {}  # for the old node's tmpF
                    for x in range(0, zeros):
                        temp = []
                        for y in range(0, x):
                            temp.append("0")
                        temp.append("1")
                        temp = baseString + "".join(temp)
                        tmpF[baseLen+x+1] = temp
                    node.UpdateF(tmpF)
                else:
                    tm = node.getF()  
                    if CopyLen in tm:
                        curOutPut = tm.pop(CopyLen)
                    else:
                        i = CopyLen - 1
                        while i not in tm:
                            i = i - 1
                        prePart = tm.pop(i)
                        baseLen = len(prePart)
                        diff = CopyLen - baseLen
                        Res = []
                        for i in range(diff):
                            Res.append('0')
                            tmp = []
                            for j in range(i):
                                tmp.append('0')
                            tmp.append('1')
                            tmp = prePart + "".join(tmp)
                            tm[baseLen + i + 1] = tmp
                        Res = prePart + "".join(Res)
                        curOutPut = Res
                    node.UpdateF(tm)
                # the new node
                # the next three lines: for the new node's space.
                curSpaceNew = []
                for i in range(0, CopyLen - 1):
                    curSpaceNew.append(0)
                curSpaceNew.append(1)
                edgeColor = randomcolor()
                NewNode = Node(curOutPut, curSpaceNew, {}, str(ancestor), Gindex, edgeColor)
                cdot.node(str(NewNode.getIndex()), str(NewNode.getIndex()), shape="point")
                cdot.edge(str(node.getIndex()), str(NewNode.getIndex()), color=node.getColor())  # dot.edge(tail, head)
                Gindex += 1
                result[selfLoc].append(NewNode)
                copyFlag = 1  # represent the copy process has succeed
                break
        if j1 == len(ancesorList):  # represent has traverse all the nodes in this request, and still not find a suitable node.
            copyLen1 = len(ancesorList[0].getString())
            ggrandFa = ancesorList[0].getPreRe()
            flag = Copy(copyLen1, ancestor, ggrandFa, result, cdot, requestdot)
            if flag:
                start = len(ancesorList) - 1
            else:
                return False
    return True

# for the color of the edge.
def randomcolor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color

# this is the main function
def main():
    global TIMES
    global GlobalSpace
    global RequestIndex
    global Gindex
    global result  # the elements in result are lists.

    starttime = time.time()
    cdot = gv.Graph("Tree")  # used for the drawing of the requirement tree.
    requestdot = gv.Graph("ReqTree")
    flag = True
    trace = []
    F = {}
    requestdot.node(str(RequestIndex), str(RequestIndex))
    RequestIndex += 1
    requestdot.node(str(RequestIndex), str(RequestIndex), shape='point')
    requestdot.edge(str(RequestIndex - 1), str(RequestIndex))
    RequestIndex += 1

    # creating the first requirement
    lenFirst = random.randint(1, 3)  # produce a random int bwtween 1 and 3.  1<=lenFirst<=3
    for x in range(0, lenFirst):
        trace.append(1)
        GlobalSpace.append(1)
        temp = []
        for y in range(0, x):
            temp.append('0')
        temp.append('1')
        F[x + 1] = "".join(temp)
    # this part is used for the space tree, the following GlobalNode represents the whole space
    # this GlobalNode is empty string
    # creating the root Node
    edgeColor1 = randomcolor()
    GlobalNode = Node("", trace, F, "*", Gindex, edgeColor1)  # this node represent the root of all requiremnt  Gindex = 0 here
    cdot.node(str(GlobalNode.getIndex()), str(GlobalNode.getIndex()), shape='point')  # add the root node.
    Gindex += 1
    globalList = []  # this list only contains one node.
    # In this program, every node belongs to one requirement, one requirement may have more than one string
    globalList.append(GlobalNode)
    result.append(globalList)  # this is the No.0 element in the requirement sequence.

    # this part is designed for the first request
    # the following part is building a node for the first requirement
    firtReqString = ""
    for i in range(0, lenFirst):
        firtReqString += "0"
    # first represents the first requirement.
    spaceFirst = []  # the left space for the new requirement node
    for i in range(0, lenFirst - 1):
        spaceFirst.append(0)
    spaceFirst.append(1)
    # the node for your first requirement
    edgeColor2 = randomcolor()
    first = Node(firtReqString, spaceFirst, {}, "0", Gindex,edgeColor2)  # the Gindex = 1 here. the first time Gindex called.
    Gindex += 1
    tmpList = []
    tmpList.append(first)
    result.append(tmpList)
    cdot.node(str(first.getIndex()), str(first.getIndex()), shape="point")
    cdot.edge(str(GlobalNode.getIndex()), str(first.getIndex()), color=GlobalNode.getColor())
    # dot.edge(tail, head)，new observation: the first node is at top

    # add the first request into the result
    times = 2
    lenLowerBound = 1

    # for more requirements
    while flag:  # executes TIMES times totally, produce TIMES requests.
        ancestor = random.randint(1, len(result) - 1)  # this function include both end parameters.
        ancestorList = result[ancestor]  # the list of Nodes. first element reslut [0] is root(has no practical meaning)
        preRLength = len(ancestorList[0].getString())

        baseLen = max(preRLength + 1, lenLowerBound)
        lengthIn = random.randint(baseLen, baseLen + MaxIncreaseLen)

        # update the GlobalSpace first
        tmpdiff = lengthIn - len(GlobalSpace)
        while tmpdiff > 0:
            GlobalSpace.append(0)
            tmpdiff -= 1
        position = lengthIn - 1
        while position >= 0 and GlobalSpace[position] != 1:
            position = position - 1
        if position == -1:
            print("there is something wrong")
            return
        GlobalSpace[position] = 0
        for x in range(position + 1, lengthIn):
            GlobalSpace[x] = 1

        # update the lenLowerBound
        firstOne = 0  #the first one in new GlobalSpace
        sum = 0
        u = lenLowerBound - 1
        steps = len(GlobalSpace)
        while sum < 2 and u < steps:
            sum += GlobalSpace[u]
            if GlobalSpace[u] == 1 and sum == 1:
                firstOne = u
            u += 1

        if sum == 2:
            if position == lenLowerBound - 1:
                lenLowerBound = firstOne + 1
        else:
            if position == lenLowerBound - 1:
                lenLowerBound = firstOne + 2
            else:
                lenLowerBound += 1
        copyFlag = 0
        start = 0
        while copyFlag == 0:
            j = start
            while j < len(ancestorList):
                node = ancestorList[j]
                curSpace = node.getSpace()  # the remaining space of the node your input point to
                tmpDiff = lengthIn - len(curSpace)
                while tmpDiff > 0:
                    tmpDiff -= 1
                    curSpace.append(0)
                
                position = lengthIn - 1
                while position >= 0 and curSpace[position] != 1:
                    position = position - 1
                if position == -1:  # means the remaining space is not enough
                    j += 1
                else:  # means the remaining space is enough
                    # update the previous node's space( the ancestor node)
                    curSpace[position] = 0
                    for x in range(position + 1, lengthIn):
                        curSpace[x] = 1
                    node.UpdateSpace(curSpace)

                    requestdot.node(str(RequestIndex), str(RequestIndex), shape='point')
                    requestdot.edge(str(ancestor), str(RequestIndex))
                    RequestIndex += 1

                    curOutPut = ""  # for the output of the request
                    # update the previous node's F set
                    if not node.getF():  # means node.getF() is empty   if node is empty, node.getF() == False
                        baseString = node.getString()  # the string of node itself, equally the new string's former part
                        baseLen = len(baseString)
                        zeros = lengthIn - len(baseString)
                        tmpx = 0
                        tmpStr = []
                        while tmpx < zeros:  # just add some zeros after the node.getString()
                            tmpx += 1
                            tmpStr.append('0')
                        
                        curOutPut = baseString + "".join(tmpStr)
                        tmpF = {}  # used to update the F set for node, cause this node has a successor
                        # zeros = lengthIn - len(node.getString()) # the Difference between lenghtIn and the len of node.getString()
                        for x in range(0, zeros):
                            temp = []
                            for y in range(0, x):
                                temp.append('0')
                            temp.append('1')
                            temp = baseString + "".join(temp)
                            tmpF[baseLen + x + 1] = temp
                        node.UpdateF(tmpF)
                    else:  # means that node.getF() is not empyt
                        tm = node.getF()  
                        if lengthIn in tm:
                            Res = tm.pop(lengthIn)
                            curOutPut = Res
                        else:
                            i = lengthIn - 1
                            while i not in tm:
                                i = i - 1
                            prePart = tm.pop(i)
                            baseLen = len(prePart)
                            diff = lengthIn - baseLen
                            Res = []
                            for i in range(diff):
                                Res.append('0')
                                tmp = []
                                for j in range(i):
                                    tmp.append('0')
                                tmp.append('1')
                                tmp = prePart + "".join(tmp)
                                tm[baseLen + i + 1] = tmp
                            Res = prePart+"".join(Res)
                            curOutPut = Res
                        node.UpdateF(tm)

                    # creating the node you require.
                    curSpaceNewNode = []
                    for i in range(0, lengthIn - 1):  # the new node's space
                        curSpaceNewNode.append(0)
                    curSpaceNewNode.append(1)  # the curSpace2's length is lengthIn
                    edgeColortmp = randomcolor()
                    NewNode = Node(curOutPut, curSpaceNewNode, {}, str(ancestor), Gindex, edgeColortmp)
                    Gindex += 1
                    tmpList2 = []
                    tmpList2.append(NewNode)
                    result.append(tmpList2)  # notice that result is a list

                    cdot.node(str(NewNode.getIndex()), str(NewNode.getIndex()), shape="point")
                    cdot.edge(str(node.getIndex()), str(NewNode.getIndex()), color=node.getColor())  # dot.edge(tail, head)
                    copyFlag = 1  #
                    break
            if j == len(ancestorList):
                copyReq = len(ancestorList[0].getString())  # represent the length of the father node
                grandFather = ancestorList[0].getPreRe()
                if Copy(copyReq, ancestor, grandFather, result, cdot, requestdot):  # means the final copy succeed
                    # ancesorList = result[ancestor]  
                    start = len(ancestorList) - 1
                else:
                    global Failure
                    Failure += 1
                    print('there is not enough space for your requirement')
                    break
        times += 1
        if times > TIMES:
            flag = False

    endtime = time.time()
    print("total time consuming:" + str(endtime - starttime))
    print("total requests:" + str(times - 1))
    print("failure times:" + str(Failure))
    print("RequestIndex:" + str(RequestIndex - 1))
    global PATH
    global PATH2
    f = open(PATH, 'w+')
    print(cdot.source, file=f)
    f2 = open(PATH2, 'w+')
    print(requestdot.source, file=f2)  # this means the requirement tree

if __name__ == '__main__':
    main()




