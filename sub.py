import redis
import time
import pandas as pd

address = redis.Redis(host="localhost", port=6379, db=0)

print('수신중 입니다. 잠시만 기다려 주세요.')
address.delete('value')
while True:
    getcolumn = address.get('column')
    getValue = address.get('value')
    if getValue is not None:
        columnData = getcolumn.decode()
        valueData = getValue.decode()

        print(columnData)
        print(valueData)

        # columnData = columnData.replace("'", '')
        # valueData = valueData.replace("'", '')

        # columnData = [columnData[1:-1].split(' ')]
        # valueData = [valueData[2:-2].split(' ')]

        # print(columnData)
        # print(valueData)

        # df = pd.DataFrame(
        #     columns=columnData,
        #     data=valueData
        # )

        # print(df)
        break
    time.sleep(0.1)