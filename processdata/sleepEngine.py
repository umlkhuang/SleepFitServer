from mysqlHelper import MysqlHelper
from datetime import datetime, timedelta
from numpy import array
from sklearn.externals import joblib
from instance import SleepLog

class SleepEngine(object):
    def __init__(self, cid, lastSensingdataTS, configurationCode = 12):
        self.mysqlHelper = MysqlHelper()
        self.cid = cid
        self.TS = lastSensingdataTS
        self.configurationCode = configurationCode
        # TODO: need to get these two list from model file
        self.predictModel = self.getPredictionModel()
        self.wifiList = self.getWifiList()
        self.appUsageList = self.getAppUsageList()
        self.timeList = list()

    def getPredictionModel(self):
        generalModelPath = "/home/ke/sleepfit/static/models/gmodel.pkl"
        self.configurationCode = 12
        predictModel = joblib.load(generalModelPath)
        return predictModel

    def getWifiList(self):
        return dict()

    def getAppUsageList(self):
        return dict()

    def getScreenOnSecondsFromAppUsage(self, appUsage):
        totalScreenOnTime = 0
        if appUsage == "":
            return totalScreenOnTime
        usageList = appUsage.split(",")
        for oneUsage in usageList:
            tmp = oneUsage.split(":")
            if len(tmp) != 3:
                continue
            else:
                totalScreenOnTime += int(tmp[2])
        return totalScreenOnTime

    def generateDataList(self, combinedData, t = 12):
        """
        Generate the final learning data array and label from the combined data instance
        """
        data = list()
        if t / 8 >= 1:
            #data.append(combinedData.month)
            data.append(combinedData.day)
            data.append(combinedData.dayOfWeek)
            data.append(combinedData.hour)
        if (t % 8) / 4 >= 1:
            data.append(combinedData.movement)
            data.append(combinedData.illuminanceMax)
            data.append(combinedData.illuminanceMin)
            data.append(combinedData.illuminanceAvg)
            data.append(combinedData.illuminanceStd)
            data.append(combinedData.decibelMax)
            data.append(combinedData.decibelMin)
            data.append(combinedData.decibelAvg)
            data.append(combinedData.decibelStd)
            data.append(combinedData.isCharging)
            data.append(combinedData.powerLevel)
            data.append(combinedData.proximity)
            data.append(self.getScreenOnSecondsFromAppUsage(combinedData.appUsage))
        if (t % 4) / 2 >= 1:
            for i in range(0, len(self.wifiList)):
                data.append(-1 * combinedData.wifiCounter[self.wifiList[i]])
        if (t % 2) == 1:
            for i in range(0, len(self.appUsageList)):
                data.append(combinedData.appUsage[self.appUsageList[i]] > 0)
        return data

    def getSleepTimeAndDuration(self, predicts, createTimeList):
        #print list(predicts)
        ret = list()
        testSize = len(predicts)
        if testSize <= 0:
            return ret
        firstValue = predicts[0]
        idx = 1
        record = dict()
        if firstValue == 1:
            record['start'] = createTimeList[0]
        while idx < testSize:
            if predicts[idx] == predicts[idx - 1]:
                # go to check the next record, increment idx by 1
                idx += 1
            else:
                # Previous record is sleep
                if predicts[idx - 1] == 1:
                    record['end'] = createTimeList[idx - 1]
                    record['duration'] = ((record['end'] - record['start']).total_seconds()) / 60
                    if len(ret) == 0:
                        ret.append(record)
                    else:
                        preSeg = ret[-1]
                        delta = (record['start'] - preSeg['end']).total_seconds() / 60
                        if delta <= 30:
                            ret[-1]['end'] = record['end']
                            ret[-1]['duration'] = (ret[-1]['end'] - ret[-1]['start']).total_seconds() / 60
                        else:
                            ret.append(record)
                # Previous record is awake
                else:
                    record = dict()
                    record['start'] = createTimeList[idx]
                    record['end'] = None
                idx += 1
        if record['start'] is not None and record['end'] is None and predicts[idx - 1] == 1:
            record['end'] = createTimeList[idx - 1]
            record['duration'] = ((record['end'] - record['start']).total_seconds()) / 60
            if len(ret) == 0:
                ret.append(record)
            else:
                preSeg = ret[-1]
                delta = (record['start'] - preSeg['end']).total_seconds() / 60
                if delta <= 30:
                    ret[-1]['end'] = record['end']
                    ret[-1]['duration'] = (ret[-1]['end'] - ret[-1]['start']).total_seconds() / 60
                else:
                    ret.append(record)
        return ret

    def calculateSleep(self):
        if self.TS is None:
            return

        hour = self.TS.hour
        if hour < 7 or hour > 9:
            return

        trackDate = self.TS.strftime("%m/%d/%Y")
        userUpdated = self.mysqlHelper.checkUserUpdatedSleep(self.cid, trackDate)
        if userUpdated:
            return

        startTS = self.TS - timedelta(seconds = 15 * 60 * 60)
        endTS = self.TS
        sensingDataList = self.mysqlHelper.getSensingDataByTime(startTS, endTS, self.cid)
        if len(sensingDataList) <= 0:
            return
        testSet = list()
        for sensingData in sensingDataList:
            self.timeList.append(sensingData.createTime)
            testSet.append(self.generateDataList(sensingData, self.configurationCode))
        testArray = array(testSet)
        predicts = self.predictModel.predict(testArray)
        #for idx in range(len(predicts)):
        #    print self.timeList[idx],
        #    print predicts[idx]
        sleepSegments = self.getSleepTimeAndDuration(predicts, self.timeList)
        sleepSegSize = len(sleepSegments)
        if sleepSegSize == 0:
            return
        lastNightSleep = dict()
        lastNightSleep['sleepTime'] = sleepSegments[0]['start']
        lastNightSleep['wakeupTime'] = sleepSegments[0]['end']
        lastNightSleep['duration'] = sleepSegments[0]['duration']
        #print sleepSegments[0]
        for idx in range(1, sleepSegSize):
            oneSleepSeg = sleepSegments[idx]
            #print oneSleepSeg
            if oneSleepSeg['duration'] > lastNightSleep['duration']:
                lastNightSleep['sleepTime'] = oneSleepSeg['start']
                lastNightSleep['wakeupTime'] = oneSleepSeg['end']
                lastNightSleep['duration'] = oneSleepSeg['duration']

        sleepInstance = SleepLog(datetime.now(), trackDate, lastNightSleep['sleepTime'], lastNightSleep['wakeupTime'], 0, 0)
        if self.mysqlHelper.checkSleepLogExists(self.cid, trackDate):
            self.mysqlHelper.updateSleepLogData(sleepInstance, self.cid)
        else:
            self.mysqlHelper.insertSleepData(sleepInstance, self.cid)



if __name__ == "__main__":
    TS = datetime(2015, 1, 3, 10, 30)
    engine = SleepEngine("6e44881f5af5d54a452b99f57899a7", TS)
    engine.calculateSleep()


