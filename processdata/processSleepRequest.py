from mysqlHelper import MysqlHelper
import simplejson as json

def get_sleep_by_day(cid, trackDate):
    mdb = MysqlHelper()
    sleepLogData = mdb.getSleepLogData(cid, trackDate)
    if len(sleepLogData) <= 0:
        return ""
    else:
        retDict = dict()
        retDict['sleepTime'] = sleepLogData[0].sleepTime.strftime('%m/%d/%Y %H:%M:%S')
        retDict['wakeupTime'] = sleepLogData[0].wakeupTime.strftime('%m/%d/%Y %H:%M:%S')
        return json.dumps(retDict)
