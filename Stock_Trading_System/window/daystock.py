import pandas as pd

# 주식 데이터 가져오기
class getDayData:
    def __init__(self, stockChart, code, name):
        self.stockChart = stockChart
        self.code = code
        self.name = name

    def getjusik(self):
        code = [] # 종목코드
        name = [] # 종목명
        c0 = []   # 날짜
        c1 = []   # 시간
        c2 = []   # 시가
        c3 = []   # 고가
        c4 = []   # 저가
        c5 = []   # 종가
        c8 = []   # 거래량

        self.stockChart.SetInputValue(0, self.code)
        self.stockChart.SetInputValue(1, ord('2'))
        self.stockChart.SetInputValue(4, 1)
        self.stockChart.SetInputValue(5, (0,1,2,3,4,5,8,9,10,11))
        self.stockChart.SetInputValue(6, ord('D'))
        self.stockChart.SetInputValue(9, ord('1'))

        self.stockChart.BlockRequest()

        numData = self.stockChart.GetHeaderValue(3)
                    
        for i in range(numData):
            code.append(self.code)
            name.append(self.name)
            c0.append(str(self.stockChart.GetDataValue(0, i)))
            c2.append(self.stockChart.GetDataValue(2, i))
            c3.append(self.stockChart.GetDataValue(3, i))
            c4.append(self.stockChart.GetDataValue(4, i))
            c5.append(self.stockChart.GetDataValue(5, i))
            c8.append(self.stockChart.GetDataValue(8, i))
        dataDf = pd.DataFrame()
        dataDf['종목코드'] = code
        dataDf['종목명'] = name
        dataDf['날짜'] = c0
        dataDf['시가'] = c2
        dataDf['고가'] = c3
        dataDf['저가'] = c4
        dataDf['종가'] = c5
        dataDf['거래량'] = c8

        dataDf.to_csv('./daystockdata/'+self.name+' 일 단위 주식 데이터.csv', encoding='euc-kr', index=False)
        print('[시스템]:'+self.name+' 종목의 일 단위 주식 데이터 요청 수신성공 및 csv로 저장 성공!')

        print('[시스템]:'+self.name+' 종목의 일 단위 주식 데이터 백업본 csv 불러오는중...')
        backUpDataDf = pd.read_csv('./hapdaystockdata/'+self.name+' 일 단위 주식 데이터.csv', encoding='euc-kr')
        hapData = pd.concat([backUpDataDf, dataDf], axis=0)
        hapData.to_csv('./hapdaystockdata/'+self.name+' 일 단위 주식 데이터.csv', encoding='euc-kr', index=False)
        print('[시스템]:'+self.name+' 종목의 일 단위 주식 데이터 백업본 업데이트 성공!')
