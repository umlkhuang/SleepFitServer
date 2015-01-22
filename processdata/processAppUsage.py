from database import DatabaseHelper
from mysqlHelper import MysqlHelper
from datetime import datetime, timedelta 
from util import Counter 
from constants import SMS_NAME, PHONECALL_NAME

import sys

def getAppUsageByHour(trackDay, cid):
    month, day, year = trackDay.split('/') 
    startTS = datetime(int(year), int(month), int(day), 0, 0, 0)
    endTS   = datetime(int(year), int(month), int(day), 23, 59, 59)
    mdb = MysqlHelper()
    sensingData = mdb.getSensingDataByTime(startTS, endTS, cid)
    
    usageTime = Counter()
    usageFreq = Counter() 
    commnTime = Counter()
    commnFreq = Counter()  
    for instance in sensingData:
        usage = instance.appUsage 
        hour  = instance.hour 
        if usage is "": continue
        usageList = usage.split(",")
        for oneUsage in usageList:
            tmp = oneUsage.split(":") 
            if len(tmp) != 3: continue
            usageTime[hour] += int(tmp[2])
            usageFreq[hour] += int(tmp[1])
            if tmp[0] == PHONECALL_NAME or tmp[0] == SMS_NAME:
                commnTime[hour] += int(tmp[2])
                commnFreq[hour] += int(tmp[1])
    t1 = list()
    t2 = list()
    t3 = list()
    t4 = list()
    t1Min = sys.maxint;
    t1Max = -1;
    t2Min = sys.maxint;
    t2Max = -1;
    t3Min = sys.maxint;
    t3Max = -1;
    t4Min = sys.maxint;
    t4Max = -1;
    for h in range(0, 24):
        t1Dict = dict() 
        t1ValDict = dict()
        t1ValDict['name'] = h
        t1ValDict['value'] = usageTime[h] / 60
        t1Dict['data'] = t1ValDict
        t1.append(t1Dict)
        if usageTime[h] > t1Max: t1Max = usageTime[h]
        if usageTime[h] < t1Min: t1Min = usageTime[h]
        
        t2Dict = dict()
        t2ValDict = dict()
        t2ValDict['name'] = h
        t2ValDict['value'] = usageFreq[h]
        t2Dict['data'] = t2ValDict
        t2.append(t2Dict)
        if usageFreq[h] > t2Max: t2Max = usageFreq[h]
        if usageFreq[h] < t2Min: t2Min = usageFreq[h]
        
        t3Dict = dict()
        t3ValDict = dict()
        t3ValDict['name'] = h
        t3ValDict['value'] = commnTime[h] / 60
        t3Dict['data'] = t3ValDict 
        t3.append(t3Dict)
        if commnTime[h] > t3Max: t3Max = commnTime[h]
        if commnTime[h] < t3Min: t3Min = commnTime[h]
        
        t4Dict = dict()
        t4ValDict = dict()
        t4ValDict['name'] = h
        t4ValDict['value'] = commnFreq[h]
        t4Dict['data'] = t4ValDict 
        t4.append(t4Dict)
        if commnFreq[h] > t4Max: t4Max = commnFreq[h]
        if commnFreq[h] < t4Min: t4Min = commnFreq[h]
    retDict = dict()
    
    t1Max /= 60
    t1Min /= 60
    t3Max /= 60
    t3Min /= 60
    
    retDict['time'] = dict()
    retDict['time']['data'] = t1
    retDict['time']['title'] = "App Usage Time"
    retDict['time']['y_suffix'] = "minute(s)"
    retDict['time']['y_min'] = t1Min
    retDict['time']['y_max'] = t1Max 
    
    retDict['index'] = dict()
    retDict['index']['data'] = t2
    retDict['index']['title'] = "App Usage Frequency"
    retDict['index']['y_suffix'] = ""
    retDict['index']['y_min'] = t2Min
    retDict['index']['y_max'] = t2Max
    
    """
    retDict['time'] = dict()
    retDict['time']['data'] = t3
    retDict['time']['title'] = "Communication Time"
    retDict['time']['y_suffix'] = "second(s)"
    retDict['time']['y_min'] = t3Min
    retDict['time']['y_max'] = t3Max
    
    retDict['index'] = dict() 
    retDict['index']['data'] = t4
    retDict['index']['title'] = "Communication Frequency"
    retDict['index']['y_suffix'] = ""
    retDict['index']['y_min'] = t4Min
    retDict['index']['y_max'] = t4Max
    """
    
    return retDict

def getAppUsageByDays(trackDay, daysNum, cid):
    month, day, year = trackDay.split('/')
    endTS   = datetime(int(year), int(month), int(day), 23, 59, 59)
    startTS = datetime(int(year), int(month), int(day), 0, 0, 0) - timedelta(days = daysNum - 1)
    mdb = MysqlHelper()
    sensingData = mdb.getSensingDataByTime(startTS, endTS, cid)
    
    usageTime = Counter()
    usageFreq = Counter() 
    commnTime = Counter()
    commnFreq = Counter()
    for instance in sensingData:
        usage = instance.appUsage
        trackDate = instance.trackDate
        if usage is "": continue
        usageList = usage.split(",")
        for oneUsage in usageList:
            tmp = oneUsage.split(":") 
            if len(tmp) != 3: continue
            usageTime[trackDate] += int(tmp[2])
            usageFreq[trackDate] += int(tmp[1])
            if tmp[0] == PHONECALL_NAME or tmp[0] == SMS_NAME:
                commnTime[trackDate] += int(tmp[2])
                commnFreq[trackDate] += int(tmp[1])
    t1 = list()
    t2 = list()
    t3 = list()
    t4 = list()
    t1Min = sys.maxint;
    t1Max = -1;
    t2Min = sys.maxint;
    t2Max = -1;
    t3Min = sys.maxint;
    t3Max = -1;
    t4Min = sys.maxint;
    t4Max = -1;
    for i in range(0, daysNum):
        trackDate = (startTS + timedelta(days = i)).strftime("%m/%d/%Y")
        t1Dict = dict() 
        t1ValDict = dict()
        t1ValDict['name'] = trackDate
        t1ValDict['value'] = usageTime[trackDate] / 60
        t1Dict['data'] = t1ValDict
        t1.append(t1Dict)
        if usageTime[trackDate] > t1Max: t1Max = usageTime[trackDate]
        if usageTime[trackDate] < t1Min: t1Min = usageTime[trackDate]
        
        t2Dict = dict()
        t2ValDict = dict()
        t2ValDict['name'] = trackDate
        t2ValDict['value'] = usageFreq[trackDate]
        t2Dict['data'] = t2ValDict
        t2.append(t2Dict)
        if usageFreq[trackDate] > t2Max: t2Max = usageFreq[trackDate]
        if usageFreq[trackDate] < t2Min: t2Min = usageFreq[trackDate]
        
        t3Dict = dict()
        t3ValDict = dict()
        t3ValDict['name'] = trackDate
        t3ValDict['value'] = commnTime[trackDate] / 60
        t3Dict['data'] = t3ValDict 
        t3.append(t3Dict)
        if commnTime[trackDate] > t3Max: t3Max = commnTime[trackDate]
        if commnTime[trackDate] < t3Min: t3Min = commnTime[trackDate]
        
        t4Dict = dict()
        t4ValDict = dict()
        t4ValDict['name'] = trackDate
        t4ValDict['value'] = commnFreq[trackDate]
        t4Dict['data'] = t4ValDict 
        t4.append(t4Dict)
        if commnFreq[trackDate] > t4Max: t4Max = commnFreq[trackDate]
        if commnFreq[trackDate] < t4Min: t4Min = commnFreq[trackDate]
    retDict = dict()
    
    t1Max /= 60
    t1Min /= 60
    t3Max /= 60
    t3Min /= 60
    
    retDict['time'] = dict()
    retDict['time']['data'] = t1
    retDict['time']['title'] = "App Usage Time"
    retDict['time']['y_suffix'] = "minute(s)"
    retDict['time']['y_min'] = t1Min
    retDict['time']['y_max'] = t1Max 
    
    retDict['index'] = dict()
    retDict['index']['data'] = t2
    retDict['index']['title'] = "App Usage Frequency"
    retDict['index']['y_suffix'] = ""
    retDict['index']['y_min'] = t2Min
    retDict['index']['y_max'] = t2Max
    
    """
    retDict['time'] = dict()
    retDict['time']['data'] = t3
    retDict['time']['title'] = "Communication Time"
    retDict['time']['y_suffix'] = "second(s)"
    retDict['time']['y_min'] = t3Min
    retDict['time']['y_max'] = t3Max
    
    retDict['index'] = dict() 
    retDict['index']['data'] = t4
    retDict['index']['title'] = "Communication Frequency"
    retDict['index']['y_suffix'] = ""
    retDict['index']['y_min'] = t4Min
    retDict['index']['y_max'] = t4Max
    """
    
    return retDict



