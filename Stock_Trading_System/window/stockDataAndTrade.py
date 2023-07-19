import win32com.client
import pandas as pd
import numpy as np
import datetime as dt
from glob import glob
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import threading
import pymysql
import time

######################################################### [주식 데이터 관련 코드] ############################################################
######################################################### [주식 데이터 관련 코드] ############################################################

# 대신증권 API 연결 확인. 1 출력시 연결 성공, 0 출력시 연결 실패
def apiConnectCheck():
    while True:
        print('[시스템]:증권사 연결 시도 중')
        if(instCpCybos.IsConnect == 1):
            print('[시스템]:증권사 연결 완료!')
            break
        else:
            print('[시스템]:증권사 연결 실패!')
            time.sleep(1)

# 증권시장에서 상장되어 있는 종목의 갯수 출력 -> 새로운 종목이 상장되거나 폐지됨에 따라 값이 달라진다.
def canTradeStockCount():
    print('[시스템]:거래 가능한 종목 개수 : '+str(instCpStockCode.GetCount())+'개 체크')

# 대신증권 기준으로 정렬된 상장된(주식거래가 가능한) 종목을 전부 가져오기
def getStockNameCode():
    print('[시스템]:거래 가능한 종목 리스트 목록 가져오는 중')
    code = [] # 종목코드
    name = [] # 종목명

    for i in range(0, instCpStockCode.GetCount()):
        code.append(instCpStockCode.GetData(0, i))
        name.append(instCpStockCode.GetData(1, i))

    codeNameList = pd.DataFrame({
        '종목코드':code
        , '종목명':name
    })
    # codeNameList
    if(len(codeNameList) == 0):
        print('[시스템]:거래 가능한 종목 리스트 목록 가져온 개수 : '+str(len(codeNameList))+'개')
        print('[시스템]:거래 가능한 종목 리스트 목록 가져오기에 문제가 발생하였습니다.')
    else:
        print('[시스템]:거래 가능한 종목 리스트 목록 가져오기 완료!')

    return codeNameList

# 원하는 종목코드, 리스트를 새로운 데이터프레임에 저장
def jongmokSerach(jongmokSearchList, codeNameList):
    code = []
    name = []
    for names in jongmokSearchList:
        code.append(codeNameList[codeNameList['종목명'] == names]['종목코드'].iloc[0])
        name.append(codeNameList[codeNameList['종목명'] == names]['종목명'].iloc[0])

    selCodeNameList = pd.DataFrame({
        '종목코드':code
        , '종목명':name
    })
    return selCodeNameList

# 주식 데이터 가져오기
def getjusik(jusikCode, jusikName):
    code = [] # 종목코드
    name = [] # 종목명
    c0 = []   # 날짜
    c1 = []   # 시간
    c2 = []   # 시가
    c3 = []   # 고가
    c4 = []   # 저가
    c5 = []   # 종가
    c8 = []   # 거래량
    c9 = []   # 거래대금
    c10 = []  # 누적체결매도수량
    c11 = []  # 누적체결매수수량

    StockChart.SetInputValue(0, jusikCode)
    StockChart.SetInputValue(1, ord('2'))
    StockChart.SetInputValue(4, 1)
    StockChart.SetInputValue(5, (0,1,2,3,4,5,8,9,10,11))
    StockChart.SetInputValue(6, ord('m'))
    StockChart.SetInputValue(9, ord('1'))

    StockChart.BlockRequest()

    numData = StockChart.GetHeaderValue(3)
                 
    for i in range(numData):
        code.append(jusikCode)
        name.append(jusikName)
        c0.append(str(StockChart.GetDataValue(0, i)))
        c1.append(str(StockChart.GetDataValue(1, i)))
        c2.append(StockChart.GetDataValue(2, i))
        c3.append(StockChart.GetDataValue(3, i))
        c4.append(StockChart.GetDataValue(4, i))
        c5.append(StockChart.GetDataValue(5, i))
        c8.append(StockChart.GetDataValue(8, i))
        c9.append(StockChart.GetDataValue(9, i))
    dataDf = pd.DataFrame()
    dataDf['종목코드'] = code
    dataDf['종목명'] = name
    dataDf['날짜'] = c0
    dataDf['시간'] = c1
    dataDf['시가'] = c2
    dataDf['고가'] = c3
    dataDf['저가'] = c4
    dataDf['종가'] = c5
    dataDf['거래량'] = c8
    dataDf['거래대금'] = c9

    return dataDf

# 주식데이터(투자주체별) 가져오기
def getjusik2(jusikCode, jusikName):
    pdListed = []

    instStockChart.SetInputValue(0, jusikCode)
    instStockChart.SetInputValue(1, 0)
    instStockChart.SetInputValue(4, ord('0'))
    instStockChart.SetInputValue(5, 0)
    instStockChart.SetInputValue(6, ord('1'))

    instStockChart.BlockRequest()

    num = instStockChart.GetHeaderValue(1)
                                                            
    for i in range(num):
        Listed = {}
        Listed['종목코드'] = jusikCode                             # 종목코드
        Listed['종목명'] = jusikName                               # 종목명
        Listed['날짜'] = instStockChart.GetDataValue(0, i)        # 날짜
        Listed['개인'] = instStockChart.GetDataValue(1, i)        # 개인
        Listed['외국인'] = instStockChart.GetDataValue(2, i)      # 외국인
        Listed['기관계'] = instStockChart.GetDataValue(3, i)      # 기관계
        Listed['금융투자'] = instStockChart.GetDataValue(4, i)    # 금융투자
        Listed['보험'] = instStockChart.GetDataValue(5, i)        # 보험
        Listed['투신'] = instStockChart.GetDataValue(6, i)        # 투신
        Listed['은행'] = instStockChart.GetDataValue(7, i)        # 은행
        Listed['기타금융'] = instStockChart.GetDataValue(8, i)    # 기타금융
        Listed['연기금'] = instStockChart.GetDataValue(9, i)      # 연기금
        Listed['기타법인'] = instStockChart.GetDataValue(10, i)   # 기타법인
        Listed['기타외인'] = instStockChart.GetDataValue(11, i)   # 기타외인
        Listed['사모펀드'] = instStockChart.GetDataValue(12, i)   # 사모펀드

        pdListed.append(Listed)

    dataDf = pd.DataFrame(pdListed)
    return dataDf

# 주식시장이 시작하고 종료되는 시간까지 실시간 분단위 데이터 가져오기
def getStockMinuteData(stockNameList, codeNameList, timeNow):
    selCodeNameList = jongmokSerach(stockNameList, codeNameList)

    print('[시스템]:종목별로 실시간 분단위 데이터 요청중')
    for j in range(0, selCodeNameList.shape[0]):
        print('[시스템]:'+str(timeNow.strftime('%Y%m%d'))+'기간에 거래된 '+str(selCodeNameList['종목명'].iloc[j])+' 종목 실시간 주가 데이터 가져오는 중')
        frame = []
        data = getjusik(selCodeNameList['종목코드'].iloc[j], selCodeNameList['종목명'].iloc[j])
        frame.append(data)
        hapdata = pd.concat(frame)
        hapdata.to_csv('./stockdata1/'+selCodeNameList['종목명'].iloc[j]+' 주식 데이터.csv', encoding='euc-kr', index=False)
        print('[시스템]:'+selCodeNameList['종목명'].iloc[j]+' 종목의 주식시세 데이터 요청 수신성공 및 csv로 저장 성공!')

# 주식시장이 시작하고 종료되는 시간까지 실시간 일단위 데이터(투자주체별) 가져오기
def getStockDayData(stockNameList, codeNameList, timeNow):
    selCodeNameList = jongmokSerach(stockNameList, codeNameList)

    for j in range(0, selCodeNameList.shape[0]):
        print('[시스템]:'+str(timeNow.strftime('%Y%m%d'))+'기간에 거래된 '+str(selCodeNameList['종목명'].iloc[j])+' 종목 주가 데이터(투자주체별) 가져오는 중')
        frame = []
        result = getjusik2(selCodeNameList['종목코드'].iloc[j], selCodeNameList['종목명'].iloc[j])
        frame.append(result)
        hapdata = pd.concat(frame)
        hapdata.to_csv('./stockdata2/'+selCodeNameList['종목명'].iloc[j]+' 주식 데이터(투자주체별).csv', encoding='euc-kr', index=False)
        print('[시스템]:'+selCodeNameList['종목명'].iloc[j]+' 종목의 주식 데이터(투자주체별) 요청 수신성공 및 csv로 저장 성공!')

# 두 주식데이터(분단위 주식 데이터, 일단위 투자주체별 데이터 합치기)
def datahap(stockNameList):
    for jongmokName in stockNameList:
        print('[시스템]:'+str(jongmokName)+' 주식 데이터 합치는 중...')
        stockData1 = pd.read_csv('./stockdata1/'+str(jongmokName)+' 주식 데이터.csv', encoding='euc-kr')
        stockData2 = pd.read_csv('./stockdata2/'+str(jongmokName)+' 주식 데이터(투자주체별).csv', encoding='euc-kr')

        colList = stockData2.columns[3:]
        valList = stockData2.values[0][3:]

        for col, val in zip(colList, valList):
            stockData1[col] = val
        stockData1.to_csv('./hapstockdata/'+str(jongmokName)+' 완성 데이터.csv', encoding='euc-kr', index=False)
    print('[시스템]:주식 데이터 합치기 완료!')

######################################################### [주식 데이터 관련 코드] ############################################################
######################################################### [주식 데이터 관련 코드] ############################################################



######################################################### [뉴스 데이터 관련 코드] ############################################################
######################################################### [뉴스 데이터 관련 코드] ############################################################

# 종목 뉴스리스트 페이지별로 전체 html코드를 긁어온 후, 리스트 형식으로 반환
def getData(code, newsPage):
    pageList = []
    for page in range(newsPage, newsPage+1):
        newsListPageUrl = 'https://finance.naver.com/item/news_news.naver?code='+str(code[1:])+'&page='+str(page)+'&sm=title_entity_id.basic&clusterId='
        data = requests.get(newsListPageUrl)
        soup = BeautifulSoup(data.content.decode('euc-kr', 'replace'), 'html.parser')
        dataFilter = soup.find('tbody')
        pageList.append(dataFilter)
    return pageList

# 뉴스페이지별로 전체 html코드를 가공하여 각 뉴스기사들의 url주소를 만들어서, 리스트 형식으로 반환
def change(bs4Data, num):
    makeUrlList = []
    newsUrlList = []
    for bs4 in bs4Data:
        change = bs4.select('tbody > tr > td > a')
        for i in range(len(change)):
            if num <= 9:
                newsUrlList.append('https://finance.naver.com'+str(change[i])[21:65]+str(change[i])[69:83]+str(change[i])[87:99]+str(change[i])[103:110]+str(change[i])[114:138])
            elif num <= 99:
                newsUrlList.append('https://finance.naver.com'+str(change[i])[21:65]+str(change[i])[69:83]+str(change[i])[87:99]+str(change[i])[103:111]+str(change[i])[115:139])
            elif num <= 999:
                newsUrlList.append('https://finance.naver.com'+str(change[i])[21:65]+str(change[i])[69:83]+str(change[i])[87:99]+str(change[i])[103:112]+str(change[i])[116:140])
    return newsUrlList

def getNewsData(urlLists):
    newsDateList = []
    newsTitleList = []
    newsTextList = []
    for i in range(len(urlLists)):
        html = requests.get(urlLists[i])
        soup = BeautifulSoup(html.content.decode('euc-kr', 'replace'), 'html.parser')
        newsDateList.append(soup.find('span',{'class':'tah p11'}).get_text())
        newsTitleList.append(soup.find('strong', {'class':'c p15'}).get_text())
        newsText = soup.find('div', {'class':'scr01'})
        if newsText.find('div', {'class':'link_news'}) != None:
            newsText.find('div', {'class':'link_news'}).decompose()
        newsTextList.append(newsText.get_text()[1:-1])
    newsDf = pd.DataFrame({
        '날짜':newsDateList
        , '제목':newsTitleList
        , '내용':newsTextList
    })
    return newsDf

def filescan(stockNameList):
    for nn in stockNameList:
        fileDataList = []
        fileList = glob('./newsdata/'+str(nn)+' 뉴스 데이터*.csv')
        for i in range(len(fileList)):
            fileDataList.append(pd.read_csv('./newsdata/'+fileList[i][11:], encoding='utf-8'))
        hapData = pd.concat(fileDataList)
        hapData.drop_duplicates(['제목'], inplace=True)
        hapData.sort_values(['날짜'], inplace=True)
        hapData.reset_index(inplace=True)
        hapData.drop('index', axis=1, inplace=True)
        hapData.to_csv('./hapnewsdata/'+str(nn)+' 뉴스 데이터.csv', encoding='utf-8', index=False)

def getNews(stockNameList, codeNameList):
    print('[시스템]:당일 뉴스 데이터 가져오는 중...')
    selCodeNameList = jongmokSerach(stockNameList, codeNameList)
    stockNewsPage = 3 # 원하는 뉴스페이지 숫자 1 ~ 999페이지까지만 긁어오기 가능. # 원하는 페이지수까지에 1을 더해서 입력해야한다.

    for numberCount in tqdm(range(1, stockNewsPage)):
        for i in range(selCodeNameList.shape[0]):
            # print(selCodeNameList['종목명'][i], selCodeNameList['종목코드'][i][1:])
            bs4Data = getData(selCodeNameList['종목코드'][i], numberCount)
            urlList = change(bs4Data, numberCount)
            getNewsDf = getNewsData(urlList)
            getNewsDf.to_csv('./newsdata/'+str(selCodeNameList['종목명'][i])+' 뉴스 데이터'+str(numberCount)+'.csv', encoding='utf-8', index=False)
    filescan(stockNameList)
    print('[시스템]:당일 뉴스 데이터 가져오기 완료!')

# 각 종목별 크롤링 해온 뉴스 데이터중에서 오늘 날짜 뉴스가 있는 지 확인
def newsSearchToday(stockNameList):
    count = 0
    for jongmokNewsName in stockNameList:
        dateList = []
        titleList = []
        textList = []
        todayNews = pd.read_csv('./hapnewsdata/'+str(jongmokNewsName)+' 뉴스 데이터.csv', encoding='utf-8')

        today = dt.datetime.now()
        #today = dt.datetime(2023,2,22)
        if today.month >= 10:
            if today.day >= 10:
                days = str(today.year)+str(today.month)+str(today.day)
            else:
                days = str(today.year)+str(today.month)+'0'+str(today.day)
        else:
            if today.day >= 10:
                days = str(today.year)+'0'+str(today.month)+str(today.day)
            else:
                days = str(today.year)+'0'+str(today.month)+'0'+str(today.day)

        for i in range(0, todayNews.shape[0]):
            newsDay = str(todayNews['날짜'][i].strip()[:4])+str(todayNews['날짜'][i].strip()[5:7])+str(todayNews['날짜'][i].strip()[8:10])
            if days == newsDay:
                dateList.append(todayNews.iloc[i]['날짜'])
                titleList.append(todayNews.iloc[i]['제목'])
                textList.append(todayNews.iloc[i]['내용'])
                count += 1

        if count > 0:
            print('[시스템]:'+str(jongmokNewsName)+' 종목의 당일 뉴스가 있음!!!')
            totoNews = pd.DataFrame({
                      '날짜':dateList
                    , '제목':titleList
                    , '내용':textList
                })
            totoNews.to_csv('./todaynewsdata/'+str(jongmokNewsName)+' 종목 오늘 날짜 뉴스.csv', encoding='utf-8', index=False)
            count = 0
        else:
            print('[시스템]:'+str(jongmokNewsName)+' 종목의 당일 뉴스가 없음.')
            totoNews = pd.DataFrame({
                      '날짜':dateList
                    , '제목':titleList
                    , '내용':textList
                })
            totoNews.to_csv('./todaynewsdata/'+str(jongmokNewsName)+' 종목 오늘 날짜 뉴스.csv', encoding='utf-8', index=False)
            count = 0

######################################################### [뉴스 데이터 관련 코드] ############################################################
######################################################### [뉴스 데이터 관련 코드] ############################################################



######################################################### [리눅스 마리아DB 관련 코드] ############################################################
######################################################### [리눅스 마리아DB 관련 코드] ############################################################

# 리눅스에 설치된 마리아DB 연결 정보
def getConn():
    conn = pymysql.connect(host='34.64.141.198', user='root', password='P@ssw0rd6388', db='stockdata')
    return conn
    
def uploadStockData(cur, conn, loadStockData, stockDataTableName):
    sql = 'insert into '+str(stockDataTableName)\
        +' (code,name,date,time,startprice,highprice,lowprice,endprice,tradecount,tradeprice)'\
        +' values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        
    for i in range(0, loadStockData.shape[0]):
        cur.execute(sql, (loadStockData['종목코드'][i],loadStockData['종목명'][i],loadStockData['날짜'][i],loadStockData['시간'][i],loadStockData['시가'][i]
                        ,loadStockData['고가'][i],loadStockData['저가'][i],loadStockData['종가'][i],loadStockData['거래량'][i],loadStockData['거래대금'][i]))
    conn.commit()

def uploadNewsData(cur, conn, loadNewsData, newsDataTableName):
    sql = 'insert into '+str(newsDataTableName)\
        +' (date,title,text)'\
        +' values (%s, %s, %s);'
    for i in range(0, loadNewsData.shape[0]):
        cur.execute(sql, (loadNewsData['날짜'][i],loadNewsData['제목'][i],loadNewsData['내용'][i]))
    conn.commit()

def uploadMariaDB(stockNameList, stockDataTableNameList, newsDataTableNameList):
    timeNow = dt.datetime.now()
    #timeNow = dt.datetime(2023,6,30,20,8)
    conn = getConn()
    cur = conn.cursor()

    if timeNow.month >= 10:
        if timeNow.day >= 10:
            dy = str(timeNow.year)+str(timeNow.month)+str(timeNow.day)
        else:
            dy = str(timeNow.year)+str(timeNow.month)+'0'+str(timeNow.day)
    else:
        if timeNow.day >= 10:
            dy = str(timeNow.year)+'0'+str(timeNow.month)+str(timeNow.day)
        else:
            dy = str(timeNow.year)+'0'+str(timeNow.month)+'0'+str(timeNow.day)

    if timeNow.hour >= 10:
        if timeNow.minute >= 10:
            times = str(timeNow.hour)+str(timeNow.minute)
        else:
            times = str(timeNow.hour)+'0'+str(timeNow.minute)
    else:
        if timeNow.minute >= 10:
            times = '0'+str(timeNow.hour)+str(timeNow.minute)
        else:
            times = '0'+str(timeNow.hour)+'0'+str(timeNow.minute)

    for nm, tn in zip(stockNameList, stockDataTableNameList):
        loadStockData = pd.read_csv('./stockdata1/'+str(nm)+' 주식 데이터.csv', encoding='euc-kr')

        if str(loadStockData['날짜'][0]) == dy:
            print('[시스템]:당일 '+str(nm)+' 종목 분단위 주식 데이터 마리아DB에 업로드 중...')
            uploadStockData(cur, conn, loadStockData, tn)
        else:
            print('[시스템]:당일 '+str(nm)+' 종목의 주식 거래된 데이터가 없어서 마리아DB에 업로드 불가!')

    for nm, tn in zip(stockNameList, newsDataTableNameList):
        loadNewsData = pd.read_csv('./todaynewsdata/'+str(nm)+' 종목 오늘 날짜 뉴스.csv', encoding='utf-8')
        if loadNewsData.shape[0] != 0:
            for i in range(loadNewsData.shape[0]):
                newsdate = str(loadNewsData['날짜'][i].strip()[:4])+str(loadNewsData['날짜'][i].strip()[5:7])+str(loadNewsData['날짜'][i].strip()[8:10])
                newstime = str(loadNewsData['날짜'][i].strip()[11:13])+str(loadNewsData['날짜'][i].strip()[14:16])

                if int(dy) == int(newsdate):
                    if int(newstime) >= int(times):
                        print('[시스템]:당일 '+str(nm)+' 종목 최신 뉴스 데이터 마리아DB에 업로드 중...')
                        uploadNewsData(cur, conn, loadNewsData, tn)
                    else:
                        print('[시스템]:당일 '+str(nm)+' 종목의 최신 뉴스 데이터가 없어서 마리아DB에 업로드 불가!')
                else:
                    print('[시스템]:당일 '+str(nm)+' 종목의 최신 뉴스 데이터가 없어서 마리아DB에 업로드 불가!')
        else:
            print('[시스템]:당일 '+str(nm)+' 종목의 최신 뉴스 데이터가 없어서 마리아DB에 업로드 불가!')

    conn.close()
    print('[시스템]:모든 데이터 업로드 완료!!!')

######################################################### [리눅스 마리아DB 관련 코드] ############################################################
######################################################### [리눅스 마리아DB 관련 코드] ############################################################


# 원하는 주식데이터를 가져올 수 있는 대신증권 모듈 선언
instCpCybos = win32com.client.Dispatch('CpUtil.CpCybos')
instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
StockChart = win32com.client.Dispatch("CpSysDib.StockChart")
instStockChart = win32com.client.Dispatch('CpSysDib.CpSvr7254')


apiConnectCheck()
canTradeStockCount()

# GST = 083450, 고영 = 098460, 싸이맥스 = 160980, 네패스= 033640, 데이타솔루션 = 263800
# 주식 테이블명 예시 = rawstockdata263800
# 뉴스 테이블명 예시 = rawnewsdata263800

stockDataTableNameList = ['testrawstockdata1','testrawstockdata2','testrawstockdata3','testrawstockdata4','testrawstockdata5']
newsDataTableNameList = ['testrawnewsdata1','testrawnewsdata2','testrawnewsdata3','testrawnewsdata4','testrawnewsdata5']
stockNameList = ['셀바스AI','투비소프트','플리토','뷰노','알체라']
codeNameList = getStockNameCode()

while True:
    timeNow = dt.datetime.now()
    if 1530 >= timeNow.hour * 100 + timeNow.minute >= 900:
        print('[시스템]:'+str(timeNow.hour)+'시 '+str(timeNow.minute)+'분 실시간 데이터 요청하는 중')
        getStockMinuteData(stockNameList, codeNameList, timeNow)
        #getStockDayData(stockNameList, codeNameList, timeNow)
        #datahap(stockNameList)
        getNews(stockNameList, codeNameList)
        newsSearchToday(stockNameList)
        uploadMariaDB(stockNameList, stockDataTableNameList, newsDataTableNameList)

        timeNow = dt.datetime.now()
        print('[시스템]:'+str(timeNow.hour)+'시 '+str(timeNow.minute + 1)+'분이 되기 기다리는 중...')
        secondLeft = 60 - int(timeNow.second)
        time.sleep(secondLeft)
    else:
        print('[시스템]:현재 주식 거래 가능한 시간이 아닙니다. 현재시간 : '+str(timeNow.hour)+'시 '+str(timeNow.minute)+'분')
        time.sleep(1)
        continue
        #break

# print('[시스템]:수신요청 종료')
# print('끝')

#apiConnectCheck_th = threading.Thread(target=apiConnectCheck, args=())
# apiConnectCheck_th.start()
# apiConnectCheck_th.join()