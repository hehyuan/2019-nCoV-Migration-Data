# -*- coding: UTF-8 -*-
import requests
import json as js
import numpy as np
import pickle

with open("cityAndId.json",'r',encoding='utf-8') as f:
    citys= js.load(f)
cityIndex = dict()
for i,city in enumerate(list(citys.keys())):
    cityIndex[city] = i
def formatStr(str):
    index1 = str.find("list")
    str = str[index1-2:-2]
    return str

def getDataFromUrl(url):
    page = requests.Session().get(url)
    str = formatStr(page.text)
    jsonStr = js.loads(str)
    return jsonStr

def getUrl(idCity,stDate,edDate):
    url = "https://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id={}&type=move_out&startDate={}&endDate={}".format(idCity,stDate,edDate)
    return url

stDate = 20200101
edDate = 20200131

factor = np.zeros((len(citys),edDate-stDate))
cnt = 0
for FromCity in citys:
    idCity = citys[FromCity]
    url = getUrl(idCity,stDate,20200201)
    res = getDataFromUrl(url)
    data = res['list']
    for i in range(stDate,edDate):
        factor[cnt,i-stDate] = data['%d'%i]
    cnt+=1
print(factor)
np.savetxt("factor.csv",factor,delimiter=',')



