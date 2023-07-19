# 뉴스 데이터 크롤링
import requests
import pandas as pd
from glob import glob
from bs4 import BeautifulSoup
import datetime as dt

import timeCh

class getNews:
    def __init__(self, code, name, newsPage, timeNow):
        self.code = code
        self.name = name
        self.newsPage = newsPage
        self.timeNow = timeNow
        print('[시스템]:당일 '+str(self.name)+' 종목 뉴스 데이터 크롤링 중...')

    def getData(self):
        # 종목 뉴스리스트 페이지별로 전체 html코드를 긁어온 후, 리스트 형식으로 반환
        pageList = []
        for page in range(1, self.newsPage):
            newsListPageUrl = 'https://finance.naver.com/item/news_news.naver?code='+str(self.code[1:])+'&page='+str(page)+'&sm=title_entity_id.basic&clusterId='
            data = requests.get(newsListPageUrl)
            soup = BeautifulSoup(data.content.decode('euc-kr', 'replace'), 'html.parser')
            dataFilter = soup.find('tbody')
            pageList.append(dataFilter)

        # 뉴스페이지별로 전체 html코드를 가공하여 각 뉴스기사들의 url주소를 만들어서, 리스트 형식으로 반환
        newsUrlList = []
        for bs4 in pageList:
            change = bs4.select('tbody > tr > td > a')
            for i in range(len(change)):
                if self.newsPage <= 9:
                    newsUrlList.append('https://finance.naver.com'+str(change[i])[21:65]+str(change[i])[69:83]+str(change[i])[87:99]+str(change[i])[103:110]+str(change[i])[114:138])
                elif self.newsPage <= 99:
                    newsUrlList.append('https://finance.naver.com'+str(change[i])[21:65]+str(change[i])[69:83]+str(change[i])[87:99]+str(change[i])[103:111]+str(change[i])[115:139])
                elif self.newsPage <= 999:
                    newsUrlList.append('https://finance.naver.com'+str(change[i])[21:65]+str(change[i])[69:83]+str(change[i])[87:99]+str(change[i])[103:112]+str(change[i])[116:140])
  
        newsDateList = []
        newsTitleList = []
        newsTextList = []
        for i in range(len(newsUrlList)):
            html = requests.get(newsUrlList[i])
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

        timeDay = timeCh.timeChange(self.timeNow).timeDay()

        newsDateList = []
        newsTitleList = []
        newsTextList = []
        for k in range(newsDf.shape[0]):
            day = str(newsDf['날짜'][k].strip()[:4])+str(newsDf['날짜'][k].strip()[5:7])+str(newsDf['날짜'][k].strip()[8:10])
            time = str(newsDf['날짜'][k].strip()[11:13])+str(newsDf['날짜'][k].strip()[14:16])
            if str(day) == str(timeDay[0]):
                time1 = dt.time(hour=int(time[0:2]), minute=int(time[2:]))
                time2 = dt.time(hour=int(timeDay[1][0:2]), minute=int(timeDay[1][2:]))
                if time1 > time2:
                    newsDateList.append(newsDf['날짜'][k].strip())
                    newsTitleList.append(newsDf['제목'][k])
                    newsTextList.append(newsDf['내용'][k])
        newsFilterDf = pd.DataFrame({
              '날짜':newsDateList
            , '제목':newsTitleList
            , '내용':newsTextList
        })

        newsFilterDf.to_csv('./newsdata/'+str(self.name)+' 뉴스 데이터.csv', encoding='utf-8', index=False)
        print('[시스템]:당일 '+str(self.name)+' 종목 뉴스 데이터 크롤링 완료!')

        print('[시스템]:'+self.name+' 종목의 뉴스 데이터 백업본 csv 불러오는중...')
        backUpDataDf = pd.read_csv('./hapnewsdata/'+self.name+' 뉴스 데이터.csv', encoding='utf-8')
        hapData = pd.concat([backUpDataDf, newsFilterDf], axis=0)
        hapData.to_csv('./hapnewsdata/'+self.name+' 뉴스 데이터.csv', encoding='utf-8', index=False)
        print('[시스템]:'+self.name+' 종목의 뉴스 데이터 백업본 업데이트 성공!')