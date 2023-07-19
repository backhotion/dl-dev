import pandas as pd
import numpy as np
import datetime as dt
from glob import glob
from tqdm import tqdm
import win32com.client
import time

import stockapicheck
import filterstockcodename
import minstock
import daystock
import news
import stocknewsdataupload
import jipyo

instCpCybos = win32com.client.Dispatch('CpUtil.CpCybos')
instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
StockChart = win32com.client.Dispatch("CpSysDib.StockChart")
instStockChart = win32com.client.Dispatch('CpSysDib.CpSvr7254')

# ['고영','GST','네패스','데이타솔루션','싸이맥스','바이오플러스','HLB','녹십자','제이엘케이','삼성바이오로직스'\
#                 ,'셀트리온','한미약품','JW중외제약','셀바스AI','투비소프트','플리토','뷰노','알체라','삼아알미늄','LG화학'\
#                 ,'솔브레인','코스모화학','KG케미칼','코스모신소재','엔켐','상신이디피','코윈테크']

stockNameList = ['셀바스AI','투비소프트','플리토','뷰노','알체라']
database = ['34.64.132.180','root','Qorgh779021!@','stockdata']
stockNewsPage = 3  # 원하는 뉴스페이지 숫자 1 ~ 999페이지까지만 긁어오기 가능. # 원하는 페이지수까지에 1을 더해서 입력해야한다.

stockapicheck.daesin(instCpCybos, instCpStockCode).apiConnectCheck()
stockapicheck.daesin(instCpCybos, instCpStockCode).canTradeStockCount()
codeNameDf = stockapicheck.daesin(instCpCybos, instCpStockCode).getStockNameCode()
filterCodeNameDf = filterstockcodename.filterCodeName(stockNameList, codeNameDf).jongmokSerach()

timeNow = dt.datetime.now()
#timeNow = dt.datetime(2022,12,7,10,15)

for i in range(filterCodeNameDf.shape[0]):
    daystock.getDayData(StockChart, filterCodeNameDf['종목코드'][i], filterCodeNameDf['종목명'][i]).getjusik()
    
for a in range(filterCodeNameDf.shape[0]):
    jipyo.jipyo(filterCodeNameDf['종목명'][a]).gaesan()

for k in range(filterCodeNameDf.shape[0]):
    stocknewsdataupload.upload(filterCodeNameDf['종목코드'][k], filterCodeNameDf['종목명'][k], database, timeNow).uploadDayStockData()

for k in range(filterCodeNameDf.shape[0]):
    stocknewsdataupload.upload(filterCodeNameDf['종목코드'][k], filterCodeNameDf['종목명'][k], database, timeNow).uploadjipyoData()

# 반복문 실행할 코드
while True:
    timeNow = dt.datetime.now()
    if 1530 >= timeNow.hour * 100 + timeNow.minute >= 900:
        for h in range(filterCodeNameDf.shape[0]):
            minstock.getMinData(StockChart, filterCodeNameDf['종목코드'][h], filterCodeNameDf['종목명'][h]).getjusik()

        for j in range(filterCodeNameDf.shape[0]):
            news.getNews(filterCodeNameDf['종목코드'][j], filterCodeNameDf['종목명'][j], stockNewsPage, timeNow).getData()
        
        for k in range(filterCodeNameDf.shape[0]):
            stocknewsdataupload.upload(filterCodeNameDf['종목코드'][k], filterCodeNameDf['종목명'][k], database, timeNow).uploadMinStockData()

        for k in range(filterCodeNameDf.shape[0]):
            stocknewsdataupload.upload(filterCodeNameDf['종목코드'][k], filterCodeNameDf['종목명'][k], database, timeNow).uploadNewsData()

        timeNow = dt.datetime.now()
        print('[시스템]:'+str(timeNow.hour)+'시 '+str(timeNow.minute + 1)+'분이 되기 기다리는 중...')
        secondLeft = 60 - int(timeNow.second)
        time.sleep(secondLeft)
    else:
        print('[시스템]:현재 주식 거래 가능한 시간이 아닙니다. 현재시간 : '+str(timeNow.hour)+'시 '+str(timeNow.minute)+'분')
        time.sleep(1)
        continue