import requests
import bs4

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
    pids = []
    pval = []
    for ths in  soup.tr("th")[4:]:
        pids += ths.a["href"]
        pval += [int(ths.span.get_text(strip=True))]
    
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
        for i in range(3,3+len(pval)):
            if line[i] != -1:
                temp += [[i,line[i]]]
        temp = sorted(temp, key=lambda x:x[1] )
        for i in reversed(range(1,len(temp))):
            temp[i][1]-=temp[i-1][1]
        for item in temp:
            line[item[0]]=item[1]
        datas[j] = line

    return datas

# contest id
def getAll(contest_id):
    url = "http://codeforces.com/contest/"+str(contest_id)+"/standings"
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text,'lxml')
    lens = len(soup("nobr"))
    ret = getTab(url)
    for i in range(2,lens+1):
        ret += getTab(url + "/page/" + str(i))
    return ret

data = getAll(956)
for i in data:
    print(i)