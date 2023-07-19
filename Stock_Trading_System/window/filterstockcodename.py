import pandas as pd

# 원하는 종목코드, 리스트를 새로운 데이터프레임에 저장
class filterCodeName:
    def __init__(self, jongmokSearchList, codeNameList):
        self.jongmokSearchList = jongmokSearchList
        self.codeNameList = codeNameList

    def jongmokSerach(self):
        code = []
        name = []
        for names in self.jongmokSearchList:
            code.append(self.codeNameList[self.codeNameList['종목명'] == names]['종목코드'].iloc[0])
            name.append(self.codeNameList[self.codeNameList['종목명'] == names]['종목명'].iloc[0])

        selCodeNameList = pd.DataFrame({
            '종목코드':code
            , '종목명':name
        })
        return selCodeNameList