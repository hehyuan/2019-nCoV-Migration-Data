# -*- coding: UTF-8 -*-
import requests
import json as js
import numpy as np
import pickle
import datetime

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

def get_in_Url(idCity,stDate,edDate):
    url = "https://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id={}&type=move_in&startDate={}&endDate={}".format(idCity,stDate,edDate)
    return url
def get_out_Url(idCity,stDate,edDate):
    url = "https://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id={}&type=move_out&startDate={}&endDate={}".format(idCity, stDate, edDate)
    return url

stDate = datetime.date(2020,1,1)
edDate = datetime.date(2020,2,2)

factor_in_2020 = np.zeros((len(citys),(edDate-stDate).days+1))
factor_out_2020 = np.zeros((len(citys),(edDate-stDate).days+1))
factor_in_2019 = np.zeros((len(citys),(edDate-stDate).days+20))
factor_out_2019 = np.zeros((len(citys),(edDate-stDate).days+20))
cnt = 0
for FromCity in citys:
    idCity = citys[FromCity]
    begin = str(stDate).replace('-','')
    end = str(edDate).replace('-','')
    url_in = get_in_Url(idCity,begin,end)
    res_in = getDataFromUrl(url_in)
    data_in = res_in['list']
    url_out = get_out_Url(idCity,begin,end)
    res_out = getDataFromUrl(url_out)
    data_out = res_out['list']
    for i in range((edDate-stDate).days+1):
        date = stDate + datetime.timedelta(days=i)
        time = str(date).replace('-','')
        factor_in_2020[cnt,i] = data_in[time]
        factor_out_2020[cnt, i] = data_out[time]
    cnt+=1

np.savetxt("factor_in_2020.csv",factor_in_2020,delimiter=',',fmt='%.4f')
np.savetxt("factor_out_2020.csv",factor_out_2020,delimiter=',',fmt='%.4f')
print(factor_in_2020,factor_out_2020)

with open("factor_in_2020.pickle", 'wb') as f:
    pickle.dump(factor_in_2020, f)

with open("factor_out_2020.pickle", 'wb') as f:
    pickle.dump(factor_out_2020, f)

# 考虑去年的数据
cnt = 0
for FromCity in citys:
    stDate = datetime.date(2019, 1, 12)
    edDate = datetime.date(2020, 2, 1)
    deltaDays = (edDate-stDate).days+1
    idCity = citys[FromCity]
    begin = str(stDate).replace('-','')
    end = str(edDate).replace('-','')
    url_in = get_in_Url(idCity,begin,end)
    res_in = getDataFromUrl(url_in)
    data_in = res_in['list']
    url_out = get_out_Url(idCity,begin,end)
    res_out = getDataFromUrl(url_out)
    data_out = res_out['list']
    for i in range(deltaDays):
        date = stDate + datetime.timedelta(days=i)
        time = str(date).replace('-','')
        try:
            factor_in_2019[cnt,i] = data_in[time]
            factor_out_2019[cnt, i] = data_out[time]
        except:
            break
    cnt+=1
factor_in_2019 = factor_in_2019[:cnt+1]
factor_out_2019 = factor_out_2019[:cnt+1]
np.savetxt("factor_in_2019.csv",factor_in_2019,delimiter=',',fmt='%.4f')
np.savetxt("factor_out_2019.csv",factor_out_2019,delimiter=',',fmt='%.4f')
print(factor_in_2019,factor_out_2019)

with open("factor_in_2019.pickle", 'wb') as f:
    pickle.dump(factor_in_2019, f)

with open("factor_out_2019.pickle", 'wb') as f:
    pickle.dump(factor_out_2019, f)