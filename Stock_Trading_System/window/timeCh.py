# 시간 편집
class timeChange:
    def __init__(self, getTime):
        self.getTime = getTime

    def timeDay(self):
        if self.getTime.month >= 10:
            if self.getTime.day >= 10:
                dy = str(self.getTime.year)+str(self.getTime.month)+str(self.getTime.day)
            else:
                dy = str(self.getTime.year)+str(self.getTime.month)+'0'+str(self.getTime.day)
        else:
            if self.getTime.day >= 10:
                dy = str(self.getTime.year)+'0'+str(self.getTime.month)+str(self.getTime.day)
            else:
                dy = str(self.getTime.year)+'0'+str(self.getTime.month)+'0'+str(self.getTime.day)

        if self.getTime.hour >= 10:
            if self.getTime.minute >= 10:
                times = str(self.getTime.hour)+str(self.getTime.minute)
            else:
                times = str(self.getTime.hour)+'0'+str(self.getTime.minute)
        else:
            if self.getTime.minute >= 10:
                times = '0'+str(self.getTime.hour)+str(self.getTime.minute)
            else:
                times = '0'+str(self.getTime.hour)+'0'+str(self.getTime.minute)
        
        return (dy, times)