import numpy as np

import fylearn.rafpc as rafpc

import pymysql


con=pymysql.connect (host='localhost',user='root',password='',port=3306,db='virtual doctor')
cmd=con.cursor()
cmd.execute("select distinct Symptoms,id from symptoms order by id")
s=cmd.fetchall()
listdata=[]
for r in s:
    listdata.append(r[0])

cmd.execute("select distinct id from disease")
s=cmd.fetchall()
print("ddd",s)
dataset=[]
Y=[]
for r in s:
    cmd.execute("select distinct Symptoms,id from symptoms where did="+str(r[0])+" order by id")
    ss=cmd.fetchall()
    row=[]
    for rr in ss:
        row.append(rr[0])
    rowdata=[]
    Y.append(r[0])
    for rrr in listdata:
        if rrr in row:
            rowdata.append(1.0)
        else:
            rowdata.append(0.0)
    print(rowdata)
    dataset.append(rowdata)
print(dataset)
print(Y)
def test_classifier(d):
    n=len(d)
    print(d)
    l = rafpc.RandomAgreementFuzzyPatternClassifier(n_protos=1, n_features=n)

    X =dataset# np.array(dataset)


    y = np.array(Y)

    l.fit(X, y)

    res= l.predict([d])
    return res

