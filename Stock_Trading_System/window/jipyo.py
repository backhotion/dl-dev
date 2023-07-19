# 주식 지표 계산
import talib
import pandas as pd

class jipyo:
    def __init__(self, name):
        self.name = name

    def gaesan(self):
        print('[시스템]:'+self.name+' 종목의 지표 데이터 생성중...')
        dayData = pd.read_csv('./hapdaystockdata/'+self.name+' 일 단위 주식 데이터.csv', encoding='euc-kr')

        code = dayData['종목코드']
        name = dayData['종목명']
        date = dayData['날짜']
        SMA5 = talib.SMA(dayData['종가'], timeperiod=5)
        SMA20 = talib.SMA(dayData['종가'], timeperiod=10)
        upper, middle, lower = talib.BBANDS(dayData['종가'], timeperiod=20)
        RSI = talib.RSI(dayData['종가'], timeperiod=14)
        macd, macdsignal, macdhist = talib.MACD(dayData['종가'], fastperiod=12, slowperiod=26, signalperiod=9)
        ar_up, ar_dn = talib.AROON(dayData['고가'], dayData['저가'], timeperiod=14)

        jipyoDf = pd.DataFrame({
              '종목코드':code
            , '종목명':name
            , '날짜':date
            , 'SMA5':SMA5
            , 'SMA20':SMA20
            , 'UPPER':upper
            , 'MAVG':middle
            , 'LOWER':lower
            , 'RSI':RSI
            , 'MACD':macd
            , 'AROONUP':ar_up
            , 'AROONDN':ar_dn
        })
        jipyoDf['SMA5'] = jipyoDf['SMA5'].astype('float64')

        jipyoDf[33:].to_csv('./jipyo/'+self.name+' 지표 데이터.csv', encoding='euc-kr', index=False)
        print('[시스템]:'+self.name+' 종목의 지표 데이터 생성중 생성 완료!')
