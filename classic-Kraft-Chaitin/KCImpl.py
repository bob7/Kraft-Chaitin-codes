def updateF(F, position, requiredLen):
    for s in F:
        if len(s) > position: 
            if s[position] == '1':
                ss = s
                F.remove(s)  
                #print("removed" + s)
                if len(ss) < requiredLen:
                    num1 = requiredLen-len(ss);
                    for i in range(0,num1):
                        ss = ss + "0";
                    print("output:"+ss);
                    for i in range(0,num1):# 
                         tt = "";
                         sss = s;
                         for j in range(0,i):
                             tt += "0";
                         sss = sss + tt;
                         sss = sss + "1";
                         F.add(sss);
                else:
                    print("output:"+s);
                break;
    return F;

def main():
    trace = "";
    inputs = input();
    inputs = int(inputs);
    F = set();
    for num in range(0,inputs):
        trace += "1";
        temp="";
        for num2 in range(0,num):
            temp += "0";
        temp += "1";
        F.add(temp);
    output = "";
    for num in range(0,inputs):
        output = output + "0";
    print("output:"+output)  #ouput
    print(F) #F set
    print("trace:"+trace)# the new trace
    while True:
        inputs = input();
        if len(inputs)==0:
            print("the input is illegal here");
            continue;
        i = int(inputs);
        num = len(trace) - i;
        if num < 0:
            num = -num;
            for x in range(0,num):
                trace = trace + "0";
        position = i - 1; #locate the position of 1
        while position >= 0 and trace[position]!= '1':
            position = position - 1;
        if position == -1:#it means resources can not meet the requirment
            print("the input is illegal here also");
            continue;
        else:
            F = updateF( F, position, i);  # update F set
            formerpart = trace[0:position];#  update trace.
            rearPart = "";
            formerpart += "0"; 
            for num in range(position+1,i):
                formerpart = formerpart + "1";
            if len(trace) == i:
                rearPart = "";
            else :
                rearPart = trace[i:];
            trace = formerpart + rearPart;

        print(F)
        print("trace:" + trace)
main()