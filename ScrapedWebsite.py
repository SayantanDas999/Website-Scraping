# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 18:49:26 2019

@author: Sayantan
"""

import requests
from bs4 import BeautifulSoup
import pandas

r_main=requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c_main=r_main.content
soup_main=BeautifulSoup(c_main,"html.parser")
page_num=soup_main.find_all("a",{"class":"Page"})[-1].text
l=[]

for page in range(0,int(page_num)*10,10):
    r=requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="+str(page)+".html", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    all=soup.find_all("div",{"class":"propertyRow"})
    for item in all:
        d={}
        d["Address"]=item.find_all("span",{"class":"propAddressCollapse"})[0].text
        d["Locality"]=item.find_all("span",{"class":"propAddressCollapse"})[1].text
        d["Price"]=item.find_all("h4",{"class":"propPrice"})[0].text.replace("\n","").replace(" ","")
        try:
            d["Beds"]=item.find("span",{"class":"infoBed"}).find("b").text
        except:
            d["Beds"]=None
        try:
            d["FullBath"]=item.find("span",{"class":"infoValueFullBath"}).find("b").text
        except:
            d["FullBath"]=None
        try:
            d["HalfBath"]=item.find("span",{"class":"infoValueHalfBath"}).find("b").text
        except:
            d["HalfBath"]=None
        try:
            d["Square Ft"]=item.find("span",{"class":"infoSqFt"}).find("b").text
        except:
            d["Square Ft"]=None
        for column_group in item.find_all("div",{"class":"columnGroup"}):
            for feature_group,feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}),column_group.find_all("span",{"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"]=feature_name.text
        l.append(d)
        
    df=pandas.DataFrame(l)
    df.to_csv("Real_Estate.csv")
