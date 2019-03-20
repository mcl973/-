import numpy as np
import mini.Dijistla as sp
import math
class method_all():
    def __init__(self,nodenum = 11):
        self.initmap = np.zeros((nodenum,nodenum))
        self.Loadij = [0.11, 0.11, 0.1, 0.12, 0.17, 0.2, 0.17,
                       0.16, 0.14, 0.25, 0.25, 0.24, 0.3, 0.22]
        # self.Delayij = [48, 25, 32, 15, 17, 38, 47, 22, 5, 37,
        #                 50, 26, 47, 45]
        self.Delayij = [0.1937993680714527, 0.2540040648119312, 0.1271125502714918, 0.18183462269821038,
                        0.4206863293186338, 0.3380733504775385, 0.3228030858947195, 0.377369398579886,
                        0.2261626365440943, 0.34807538535028737,
                        0.572568032597279, 0.2978922416173892, 0.15322597466080183, 0.3129914666351893]
        self.Cij = [460,470,490,380,450,350,450,550,280,430,440,360,450,450]
        self.maxbw=[500,560,800,660,900,700,800,750,600,800,800,800,800,900]
        self.nodes = []
        if nodenum == 11:
            self.nodes=[[1,2],[1,3],[1,4],[1,5],[2,6],[2,7],[3,6],[4,9],[5,9],[6,8],[7,10],
                    [8,9],[8,10],[9,10]]
        elif nodenum == 10:
            self.nodes = [[0, 1], [0, 2], [0, 3], [0, 4], [1, 5], [1, 6], [2, 5], [3, 8], [4, 8], [5, 7], [6, 9],
                          [7, 8], [7, 9], [8, 9]]

        self.D0 = max(self.Delayij)
        self.lastvi = 0
        # self.initmap = self.fuzhi(self.initmap,self.Cij,self.Delayij,self.Loadij,a,b,c)
        # print(self.initmap)

    def fuzhi(self, map, cij, delay, load, a, b, c):
        i = 0
        _ = float('inf')
        for j in self.nodes:
            self.writedata(map, j[0], j[1], cij[i], delay[i], load[i], cij, delay, load, a, b, c)
            self.writedata(map, j[1], j[0], cij[i], delay[i], load[i], cij, delay, load, a, b, c)
            i += 1
        for i in range(len(map)):
            for j in range(len(map)):
                if map[i][j] == 0:
                    map[i][j] = _
        return map


    def writedata(self, map, i, j, bw, de, diu, cij, Delayij, Loadij, a, b, c):
        map[i][j] = self.quanzhi(bw, de, diu, cij, Delayij, Loadij, a, b, c)


    def getabc(self, a=0.1, b=0.3, c=0.6):
        return a, b, c


    def quanzhi(self, bw, de, diu, cij, Delayij, Loadij, a, b, c):
        Cri = bw / self.average(cij)
        Dri = de / self.average(Delayij)
        Lri = diu / self.average(Loadij)
        # 自设权重指标

        # lpri=(a*Lri+b*Dri)/(c*Cri);
        return (a * Lri + b * Dri) / (c * Cri)


    def average(self, k):
        return sum(k) / len(k)

    def getshorstpath(self,path,map,threat,uui):
        allpath={}
        num = 0
        while len(path)>1:
            # print("最短路径：", self.path)
            allpath.setdefault(num,[])
            allpath[num] = path
            # print(self.allpath)
            self.dellink2(num,path,map,threat,uui)
            path, map = sp.Dijistla(map,1,10).map()
            print(path)
            num+=1
        return allpath
    #更改map
    def dellink(self,path,map):
        _ = float("inf")
        k = len(path)
        # print(k)
        for i in range(k):
            if i+1==k:
                break
            map[path[i]][path[i+1]] = _
            map[path[i+1]][path[i]] = _
        return map
    #更改map和权值
    def dellink2(self,num,path,map,threat,uui):
        _ = float("inf")
        k = len(path)
        Upi = 1000
        uui.setdefault(num,[])

        # print(k)
        for i in range(k):
            if i+1==k:
                break
            try:
                k1 = self.nodes.index([path[i],path[i+1]])
            except:
                k1 = self.nodes.index([path[i+1],path[i]])
            # 计算UPi即最大的利用率

            bwmax = (self.maxbw[k1]- self.Cij[k1])/self.maxbw[k1]*2*self.D0/self.Delayij[k1]
            temp =  (self.maxbw[k1]- self.Cij[k1])/self.maxbw[k1]
            uui[num].append((temp,k1))

            if  bwmax<Upi:
                Upi = bwmax

            map[path[i]][path[i+1]] = _
            threat.append(Upi)

    def getrate(self,list,allrate):
        all = 0
        for i in list:
            all+=i
        k = len(list)
        for i in range(k):
            allrate.append(list[i]/all)

    def wanshanUpi(self, path, list):
        k = len(path)
        for i in range(k):
            self.kk(path[i], list)

    def kk(self, path, list):
        k = len(path)
        for i in range(k):
            if i + 1 == k:
                break
            try:
                list.append([path[i], path[i + 1]])
            except:
                list.append([path[i + 1], path[i]])

    def updaremap(self,map,cij,delay,load,a,b,c):
        i = 0
        _ = float('inf')
        nodes = self.nodes
        cij = self.Cij
        delay = self.Delayij
        load = self.Loadij

        for j in nodes:
            self.writedata(map,j[0], j[1],cij[i],delay[i],load[i],cij,delay,load,a,b,c)
            self.writedata(map,j[1], j[0],cij[i],delay[i],load[i],cij,delay,load,a,b,c)
            i += 1

        for i in range(len(map)):
            for j in range(len(map)):
                if map[i][j] == 0:
                    map[i][j] = _
        return map

    def result(self,path,threat,list):
        # list = [50, 100, 150, 200, 250,300,350,400,450,500]
        # vi =0
        k = len(path)
        resultlist = []
        while True:
            for i in range(k):
                vi = self.returnresult(list,threat[i],path[i],i)
                print(vi)
                resultlist.append(vi)
            m=0
            flag = []
            for j in resultlist:
                if j == -1 :
                    print("第"+str(m)+"条路径时延太大")
                    m += 1
                    continue
                if j == -2 :
                    print("第"+str(m)+"条路径带宽不够")
                    m += 1
                    continue
                if j == 0:
                    m += 1
                    continue
                flag.append(1)
            if len(flag) == k:
                return resultlist

    def returnresult(self,list,threat,path,k):
        vi = 100
        num = 0
        while True:
            # print(str(threat) + "  ,   " + str(vi))
            if math.fabs(threat - vi) < 0.09:
                if vi > threat:
                    return self.lastvi
                print(str(threat)+"  ,   "+str(vi))
                return vi
            if num > len(list)-1:
                num=0
            value = list[num]
            vi = self.getMaxVi(value,path,k,threat)
            if vi == self.lastvi and self.isoutbw == 1:
                self.isoutbw = 0
                return vi
            #是否超过了threat
            if self.isoutthreat == 1:
                self.isoutthreat=0
                return vi

            if vi == -1:
                print("延时太大")
            elif vi == -2:
                print("带宽不够")
                return vi
            num+=1
    def getMaxVi(self,b2,path,a,threat,cij,delay,uui):
        k = len(path)
        Vi = 0
        for i in range(k):
            if i+1==k:
                break
            try:
                k1 = self.nodes.index([path[i], path[i + 1]])
            except:
                k1 = self.nodes.index([path[i+1], path[i]])
            #计算Vi
            b1 = self.maxbw[k1] - cij[k1]
            # print("k1  "+str(k1)+"  b1   "+str(b1)+"    b2   "+ str(b2) +"  "+str(sets.setting().maxbw[k1]))

            vi = b1/self.maxbw[k1]
            #区最大的vi
            if vi>Vi:
                if vi > threat :
                    self.isoutthreat = 1
                    continue
                Vi = vi

        k = len(uui[a])
        # print(k)
        Utlist = []
        Ut=0
        # 判断条件 总延时小于 Dci

        for i in range(k):
            try:
                k1 = self.nodes.index([path[i], path[i + 1]])
                Ut = delay[k1]/(1-uui[a][i][0])
                if Ut > (self.D0 * 2):
                    return -1
                # print(self.uui[a][i][1])
                delay[uui[a][i][1]] = Ut
                # 判断条件 剩余带宽大于要分配的带宽
                if cij[uui[a][i][1]]>b2:
                    self.lastvi = Vi
                    cij[uui[a][i][1]]-=b2
                else:
                    self.isoutbw = 1
                    return self.lastvi
            except:
                pass
            return Vi

    def updatepath(self,bw,path,rate,list,cij,delay):
        paths = path
        m = len(paths)
        for j in range(m):
            if j+1==m:
                break
            try:
                k1 = self.nodes.index([paths[j],paths[j+1]])
            except:
                k1 = self.nodes.index([paths[j+1],paths[j]])
            self.Cij[k1]= self.Cij[k1]-bw*rate
            tempdelay = (self.maxbw[k1] - cij[k1]) / self.maxbw[k1]
            Ut = delay[k1] / (1 - tempdelay)
            list.append(tempdelay)
            delay[k1] = Ut
