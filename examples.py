import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from sklearn.linear_model import LinearRegression
import datetime as date
from dateutil.relativedelta import relativedelta
from io import BytesIO

def accounting() :
        i = input("종목명 : ")
        firm_code = firmdata.loc[firmdata["종목명"] == i, "종목코드"]
        firm_url = "https://comp.fnguide.com/SVO2/asp/SVD_Finance.asp?pGB=1&gicode=A" + str(firm_code)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
        firm_data = requests.get(firm_url, headers=headers)
        
        firm_data = BeautifulSoup(firm_data.content, "html.parser")
        firm_data = pd.read_html(str(firm_data), displayed_only=False)
        
        #
        data_IS = firm_data[0].copy()
        data_IS.iloc[:, 0] = data_IS.iloc[:, 0].str.replace("계산에 참여한 계정 펼치기", "")
        data_IS = data_IS.drop_duplicates()
        data_IS.index = data_IS.iloc[:, 0]
        data_IS = data_IS.iloc[:, 1:5]
        
        data_BS = firm_data[2].copy()
        data_BS.iloc[:, 0] = data_BS.iloc[:, 0].str.replace("계산에 참여한 계정 펼치기", "")
        data_BS = data_BS.drop_duplicates()
        data_BS.index = data_BS.iloc[:, 0]
        data_BS = data_BS.iloc[:, 1:5]
        
        data_CF = firm_data[4].copy()
        data_CF.iloc[:, 0] = data_CF.iloc[:, 0].str.replace("계산에 참여한 계정 펼치기", "")
        data_CF = data_CF.drop_duplicates()
        data_CF.index = data_CF.iloc[:, 0]
        data_CF = data_CF.iloc[:, 1:5]

        ##
        data_IS2 = firm_data[1]
        data_IS2.iloc[:, 0] = data_IS2.iloc[:, 0].str.replace('계산에 참여한 계정 펼치기', '')
        data_IS2 = data_IS2.drop_duplicates()
        data_IS2 = data_IS2.iloc[:,1:5]
        data_IS2['sum'] = data_IS2.sum(axis=1)
        data_IS2.index = data_IS.index

        data_IS.iloc[:,len(data_IS.columns)-1] = data_IS2['sum']


        data_CF2 = firm_data[5]
        data_CF2.iloc[:, 0] = data_CF2.iloc[:, 0].str.replace('계산에 참여한 계정 펼치기', '')
        data_CF2 = data_CF2.drop_duplicates()
        data_CF2 = data_CF2.iloc[:,1:5]
        data_CF2['sum'] = data_CF2.sum(axis=1)
        data_CF2.index = data_CF.index

        data_CF.iloc[:,len(data_CF.columns)-1] = data_CF2['sum']

        data_IS = data_IS.dropna()
        data_BS = data_BS.dropna()
        data_CF = data_CF.dropna()

        return data_IS, data_BS, data_CF
