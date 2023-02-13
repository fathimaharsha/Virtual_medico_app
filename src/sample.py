# from datetime import timedelta,date
# import calendar
# import datetime
#
# def daterange(d1,d2):
#     for n in range(int((d2-d1).days)+1):
#         yield d1+timedelta(n)
# sd=date(2020,2,16)
# ed=date(2020,2,28)
# for dt in daterange(sd,ed):
#     s=dt.strftime("%Y-%m-%d")
#
#     b=datetime.datetime.strptime(s,'%Y-%m-%d').weekday()
#     ss=calendar.day_name[b]
#     print(s,"=",ss.lower())


from os import walk
import os

import numpy as np

from src.featureextract import glcm_feat
def train():
    data=[]
    samples=[]
    names=[]
    for dir,d_path,filnames in walk("static/normal"):
      for file in filnames:
          sample=glcm_feat(os.path.join(dir,file))
          names.append(1)
          samples.append(sample)
    for dir,d_path,filnames in walk("static/cancer"):
          for file in filnames:
            sample=glcm_feat(os.path.join(dir,file))
            names.append(2)
            samples.append(sample)
    np.savetxt("sample.data",samples)
    np.savetxt("labels.dat",names)
train()