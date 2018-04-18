import requests
import bs4
import scipy.io as scio
import numpy as np

# problemid(int) solvetime(int seconds used to solve this)
def hardness(problemid,score,solvetime):
    if score == None:
        return -1
    solvetime = int(solvetime[:2])*60+int(solvetime[3:])
    return int(solvetime)

def getTab(url):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text,'lxml')
    datas = []
    ptitle = []
    for ths in  soup.tr("th")[4:]:
        ptitle += [ths.a["title"][4:]]
    
    for tr in soup(participantid = True):
        tds = tr("td")
        ret = []
        ret += [tds[1].get_text(strip=True)]
        ret += [int(tds[2].get_text(strip=True))]
        ret += [tds[3].get_text(strip=True)+""]
        for i in range(4,len(tds)):
            ret += [hardness(i,
                            tds[i](class_="cell-passed-system-test")[0].get_text(strip=True) 
                            if len(tds[i](class_="cell-passed-system-test")) != 0 
                            else None,
                            tds[i](class_="cell-time")[0].get_text(strip=True) 
                            if len(tds[i](class_="cell-time")) !=0 
                            else None )]
        datas += [ret]
    
    for j, line in enumerate(datas):
        temp = []
        for i in range(3,3+len(ptitle)):
            if line[i] != -1:
                temp += [[i,line[i]]]
        temp = sorted(temp, key=lambda x:x[1] )
        for i in reversed(range(1,len(temp))):
            temp[i][1]-=temp[i-1][1]
        for item in temp:
            line[item[0]]=item[1]
        datas[j] = line

    return datas,ptitle

# contest id
def getAll(contest_id):
    print("starting to get Contest "+str(contest_id))
    url = "http://codeforces.com/contest/"+str(contest_id)+"/standings"
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text,'lxml')
    lens = len(soup("nobr"))
    ret,title = getTab(url)
    for i in range(2,lens+1):
        print("%"+str((i-1)/lens*100)+" finished")
        nret,_ = getTab(url + "/page/" + str(i))
        ret += nret
    print("all finished")
    return ret,title

def saveRound(contest_id):
    data,title = getAll(contest_id)
    data = np.array(data)
    data = np.asmatrix(data)
    dataFile = path+str(contest_id)+'.mat'
    scio.savemat(dataFile, {str(contest_id):data})
    with open(path+"names.txt","a") as f:
        print(",".join([str(contest_id)] + title),file = f )


path = "C:/Users/wkl31415926/OneDrive/Projects/CPRS/datas/"
with open(path+"rounds.txt","r") as f:
    while True:
        line = f.readline()
        if line == "":
            break
        saveRound(int(line))

tab ={}
problems = {}
usr = {}

with open(path+"rounds.txt","r") as f:
    names={}
    with open(path+"names.txt","r") as fn:
        while True:
            line = fn.readline()
            if line == "":
                break
            temp = line.strip().split(",")
            names[int(temp[0])]=temp[1:]
        cnt = 0
        cnt2 = 0
        for i in names:
            for j in names[i]:
                if not j in problems:
                    problems[j]=cnt
                    cnt += 1
        for i in names:
            data = scio.loadmat(path+str(i)+".mat")[str(i)]
            for j in data:
                j = np.array(j).tolist()
                if not j[0] in usr:
                    usr[j[0]] = cnt2
                    tab[j[0]] = {}
                    cnt2 += 1
                for k in range(len(j[3:])):
                    if int(j[3+k]) != -1 :
                        tab[j[0]][names[i][k]] = j[3+k]
        hval = np.zeros((len(usr),len(problems)))
        val = np.zeros((len(usr),len(problems)))
        for i in tab:
            for j in tab[i]:
                hval[usr[i],problems[j]] = 1
                val[usr[i],problems[j]] = tab[i][j]
        dataFile = path+'CF.mat'
        prb = np.asmatrix(np.array(list(problems.keys())))
        user = np.asmatrix(np.array(list(usr.keys())))
        scio.savemat(dataFile, {"has_value":hval, "value":val, "problems":prb, "users":user})

        print("OK")