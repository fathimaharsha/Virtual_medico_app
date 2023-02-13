



import numpy as np

import random
from collections import Counter
# from sklearn import preprocessing
import time

import pymysql


con=pymysql.connect (host='localhost',user='root',password='',port=3306,db='virtual doctor')
cmd=con.cursor()
cmd.execute("select distinct Symptoms from symptoms order by id")
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


class CKNN:

    def __init__(self):
        self.accurate_predictions = 0
        self.total_predictions = 0
        self.accuracy = 0.0
        ##########

        lines=[]



        training_data=dataset

        self.training_set= { }
        for r in Y:
            self.training_set[str(r)]=[]


        test_data = []#[-int(test_size * len(dataset)):]

        #Insert data into the training set
        cnt=0

        for record in training_data:
            st=Y[cnt]
            cnt+=1


            self.training_set[str(st)].append( record[:])

    #########

    def predict(self,  to_predict, k = 1):


        distributions = []
        for group in self.training_set:
            i=0
            # print(group,'group')
            for features in self.training_set[group]:

                euclidean_distance = np.linalg.norm(np.array(features)- np.array(to_predict))

                distributions.append([euclidean_distance, group])

                print([euclidean_distance, group])

        # print(distributions)
        results = [i[1] for i in sorted(distributions)[:k]]
        result = Counter(results).most_common(1)[0][0]
        # print("rs",results,self.training_set.keys())
        confidence = Counter(results).most_common(1)[0][1]/k

        return result, confidence


def prep(filename):




    knn = CKNN()
    print("fname",filename)
    res=knn.predict(filename)
    print(res)




    return res[0]



# prep(r'static\data1\Citrus Reticulata Blanco\3567.jpg')
