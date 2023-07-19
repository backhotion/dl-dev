import pandas as pd
import time

class daesin:
    def __init__(self, instCpCybos, instCpStockCode):
        self.instCpCybos = instCpCybos
        self.instCpStockCode = instCpStockCode

    def apiConnectCheck(self):
        while True:
            print('[시스템]:분 단위 주식 데이터 요청 전, 증권사 연결 시도 중')
            if(self.instCpCybos.IsConnect == 1):
                print('[시스템]:증권사 연결 완료!')
                break
            else:
                print('[시스템]:증권사 연결 실패!')
                time.sleep(1)
    
    def canTradeStockCount(self):
        print('[시스템]:현재 거래 가능한 종목 개수 : '+str(self.instCpStockCode.GetCount())+'개 체크')

    def getStockNameCode(self):
        print('[시스템]:거래 가능한 종목 리스트 목록 가져오는 중')
        code = [] # 종목코드
        name = [] # 종목명

        for i in range(0, self.instCpStockCode.GetCount()):
            code.append(self.instCpStockCode.GetData(0, i))
            name.append(self.instCpStockCode.GetData(1, i))

        codeNameList = pd.DataFrame({
            '종목코드':code
            , '종목명':name
        })
        # codeNameList
        if(len(codeNameList) == 0):
            print('[시스템]:거래 가능한 종목 리스트 목록 가져온 개수 : '+str(len(codeNameList))+'개')
            print('[시스템]:거래 가능한 종목 리스트 목록 가져오기에 문제가 발생하였습니다.')
        else:
            print('[시스템]:거래 가능한 종목 리스트 목록 가져온 개수 : '+str(len(codeNameList))+'개')
            print('[시스템]:거래 가능한 종목 리스트 목록 가져오기 완료!')

        return codeNameList