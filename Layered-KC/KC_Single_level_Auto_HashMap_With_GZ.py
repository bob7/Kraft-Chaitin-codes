import random
import time
import graphviz as gv
TIMES = 50000  # represent the requests number, suggest no more than 100000
MaxIncrease = 5  # randLen = RandInt(lowerBound, lowerBound + MaxIncrease)
FileName = ".\\HashMap_KC_Auto_With_GZ.gv"  # Location of file storage
'''
NOTE:
In this program, the node is restored in the cdot Tree, 
every node has a Id and a label, 
the id means the sequence of the request, 
the label means the request length.

In this program, I add some time indicator. You can see the output,
the most time was spent on the building of the cdot tree and the output of the cdot file.
'''

def main():
    starttime = time.time()
    cdot = gv.Graph("Tree")
    lowBound = 1
    trace = []  # the global space indicator
    lenFirst = random.randint(1, 7)  # the first requirement length is 1<= lenFirst <=3
    times = 1  # recording how many requests have been put up
    F = {}  # the hashMap used to record the assistant strings
    for i in range(0, lenFirst):
        trace.append(1)
        temp = ""
        for j in range(0, i):
            temp += "0"
        temp += "1"
        F[i+1] = temp
    output = []
    for num in range(0, lenFirst):
        output.append('0');
    output = "".join(output)

    cdot.node(str(0), 'root', shape="point")
    cdot.node(str(times), str(lenFirst), shape="point")
    cdot.edge(str(0), str(times))

    totalLookUpTime = 0
    totalUpdateTime = 0
    totalFindBoundTime = 0
    totalIndexTime = 0

    while times < TIMES:
        times += 1
        randLen = random.randint(lowBound, lowBound + MaxIncrease)
        diff = randLen - len(trace)
        while diff > 0:
            trace.append(0)
            diff -= 1
        position = randLen - 1;  # locate the position of 1 which has the largest position
        while position != -1 and trace[position] != 1:
            position = position - 1

        # the following 6 lines code will never be excuted in normal condition
        if position == -1:
            print("illegal ")
            print("trace:"+str(trace))
            print("LB:"+str(lowBound))
            print("randLen:"+str(randLen))
            return

        # update the trace First
        trace[position] = 0
        for i in range(position + 1, randLen):
            trace[i] = 1

        t1 = time.time()
        firstOne = 0
        sum = 0
        u = lowBound - 1
        steps = len(trace)
        while sum < 2 and u < steps:
            sum += trace[u]
            if trace[u] == 1 and sum == 1:
                firstOne = u
            u += 1
        t2 = time.time()
        totalFindBoundTime += (t2 - t1)

        if sum == 2:
            t3 = time.time()
            if position == lowBound -1:
                lowBound = firstOne+1
            t31 = time.time()
            totalIndexTime += t31-t3
        else:
            t3 = time.time()
            if position == lowBound -1:
                lowBound = firstOne + 2
            else:
                lowBound += 1
            t31 = time.time()
            totalIndexTime += t31 - t3

        if randLen in F:
            Res = F.pop(randLen)
        else:
            t1 = time.time()
            i = randLen - 1
            while i not in F:
                i = i-1
            t2 = time.time()
            totalLookUpTime += (t2-t1)

            t3 = time.time()
            prePart = F.pop(i)
            Res = list(prePart)
            baseLen = len(prePart)
            diff = randLen - baseLen
            for i in range(diff):
                Res.append('0')
                tmp = []
                for j in range(i):
                    tmp.append('0')
                tmp.append('1')
                tmp = prePart + "".join(tmp)
                F[baseLen+i+1] = tmp
            t4 = time.time()
            totalUpdateTime += t4 - t3

        Res = "".join(Res)
        cdot.node(str(times), str(randLen), shape="point")
        cdot.edge(str(0), str(times))

    endtime = time.time()
    print("total process time:" + str(endtime - starttime))
    print("totalLookUpTime:" + str(totalLookUpTime))
    print("totalUpdateTime:" + str(totalUpdateTime))
    print("totalFindBoundTime:" + str(totalFindBoundTime))
    print("totalIndexTime:" + str(totalIndexTime))

    # this part is used to write the result into file
    global FileName
    writeBeginTime = time.time()
    f = open(FileName, 'w+')
    print(cdot.source, file=f)
    writeEndTime = time.time()
    print("writing file seconds:"+str(writeEndTime - writeBeginTime))

if __name__ == '__main__':
    main()