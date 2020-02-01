# -*- coding: UTF-8 -*-
import requests
import json as js
import numpy as np
import pickle
import datetime

def formatStr(str):
    index1 = str.find("list")
    str = str[index1-2:-2]
    return str

def getDataFromUrl(url):
    page = requests.Session().get(url)
    str = formatStr(page.text)
    jsonStr = js.loads(str)
    return jsonStr

def getUrlFromCity(idCity):
    url = "https://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id={}&type=move_out&date=".format(idCity)
    return url

if __name__ == "__main__":
    with open("cityAndId.json", 'r', encoding='utf-8') as f:
        citys = js.load(f)
    cityIndex = dict()
    for i, city in enumerate(list(citys.keys())):
        cityIndex[city] = i
    begin = datetime.date(2019,12,31)#开始日期
    end = datetime.date(2020,1,1)# 结束日期
    Tensor = dict()
    for i in range((end - begin).days + 1):
        date = begin + datetime.timedelta(days=i)
        matrix = np.zeros((len(citys),len(citys)))
        time = str(date).replace('-','')
        for FromCity in citys:
            idCity = citys[FromCity]
            url = getUrlFromCity(idCity)+(time)
            res = getDataFromUrl(url)
            data = res['list']
            for line in data:
                city = line['city_name']
                value = line['value']
                try:
                    toCity = cityIndex[city]
                    fromCity = cityIndex[FromCity]
                    matrix[fromCity, toCity] = value
                except:
                    ...
        print(date)
        print(matrix)
        Tensor[date] = matrix
        # np.savetxt("M{}".format(time)+".csv",matrix,delimiter=',',fmt='%.4f')

    # with open("dicOfMatrix.pickle",'wb') as f:
    #     pickle.dump(Tensor,f)
    # f.close()