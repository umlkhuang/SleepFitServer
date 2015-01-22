from database import DatabaseHelper
from mysqlHelper import MysqlHelper
from datetime import datetime, timedelta 
from util import Counter 
from constants import SEDENTARY_MAX_COUNT, ACTIVE_MIN_COUNT

import sys

def getMobilityByHour(trackDay, cid):
    month, day, year = trackDay.split('/') 
    startTS = datetime(int(year), int(month), int(day), 0, 0, 0)
    endTS   = datetime(int(year), int(month), int(day), 23, 59, 59) 
    
    sedentaryTime  = Counter()
    sedentaryIndex = Counter()
    activeTime     = Counter()
    activeIndex    = Counter()  
    
    mdb = MysqlHelper()
    sensingData = mdb.getSensingDataByTime(startTS, endTS, cid) 
    
    for instance in sensingData:
        hour = instance.hour 
        movement = instance.movement 
        if movement <= SEDENTARY_MAX_COUNT:
            sedentaryTime[hour] += 5
            sedentaryIndex[hour] += movement
        elif movement >= ACTIVE_MIN_COUNT:
            activeTime[hour] += 5
            activeIndex[hour] += movement 
    
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
        t1ValDict['value'] = sedentaryTime[h] 
        t1Dict['data'] = t1ValDict
        t1.append(t1Dict)
        if (sedentaryTime[h] > t1Max): t1Max = sedentaryTime[h]
        if (sedentaryTime[h] < t1Min): t1Min = sedentaryTime[h] 
        
        t2Dict = dict()
        t2ValDict = dict()
        t2ValDict['name'] = h
        t2ValDict['value'] = sedentaryIndex[h]
        t2Dict['data'] = t2ValDict
        t2.append(t2Dict)
        if (sedentaryIndex[h] > t2Max): t2Max = sedentaryIndex[h]
        if (sedentaryIndex[h] < t2Min): t2Min = sedentaryIndex[h] 
        
        t3Dict = dict()
        t3ValDict = dict()
        t3ValDict['name'] = h
        t3ValDict['value'] = activeTime[h]
        t3Dict['data'] = t3ValDict 
        t3.append(t3Dict)
        if (activeTime[h] > t3Max): t3Max = activeTime[h]
        if (activeTime[h] < t3Min): t3Min = activeTime[h] 
        
        t4Dict = dict()
        t4ValDict = dict()
        t4ValDict['name'] = h
        t4ValDict['value'] = activeIndex[h]
        t4Dict['data'] = t4ValDict 
        t4.append(t4Dict)
        if (activeIndex[h] > t4Max): t4Max = activeIndex[h]
        if (activeIndex[h] < t4Min): t4Min = activeIndex[h] 
    mobility = dict()
    """
    mobility['sedentary_time'] = dict() 
    mobility['sedentary_time']['data'] = t1
    mobility['sedentary_time']['title'] = "Sedentary Time"
    mobility['sedentary_time']['y_suffix'] = "minute(s)"
    mobility['sedentary_time']['y_min'] = t1Min
    mobility['sedentary_time']['y_max'] = t1Max 
    
    mobility['sedentary_index'] = dict()
    mobility['sedentary_index']['data'] = t2 
    mobility['sedentary_index']['title'] = "Sedentary Index"
    mobility['sedentary_index']['y_suffix'] = ""
    mobility['sedentary_index']['y_min'] = t2Min
    mobility['sedentary_index']['y_max'] = t2Max
    """
    
    mobility['time'] = dict() 
    mobility['time']['data'] = t3
    mobility['time']['title'] = "Active Time"
    mobility['time']['y_suffix'] = "minutes(s)"
    mobility['time']['y_min'] = t3Min
    mobility['time']['y_max'] = t3Max 
    
    mobility['index'] = dict() 
    mobility['index']['data'] = t4
    mobility['index']['title'] = "Active Index"
    mobility['index']['y_suffix'] = ""
    mobility['index']['y_min'] = t4Min
    mobility['index']['y_max'] = t4Max
    
    return mobility
    
def getMobilityByDays(trackDay, daysNum, cid):
    month, day, year = trackDay.split('/')
    endTS   = datetime(int(year), int(month), int(day), 23, 59, 59)
    startTS = datetime(int(year), int(month), int(day), 0, 0, 0) - timedelta(days = daysNum - 1) 
    
    sedentaryTime  = Counter()
    sedentaryIndex = Counter()
    activeTime     = Counter()
    activeIndex    = Counter()  
    
    mdb = MysqlHelper()
    sensingData = mdb.getSensingDataByTime(startTS, endTS, cid) 
    
    for instance in sensingData:
        trackDate = instance.trackDate 
        movement = instance.movement 
        if movement <= SEDENTARY_MAX_COUNT:
            sedentaryTime[trackDate] += 5
            sedentaryIndex[trackDate] += movement
        elif movement >= ACTIVE_MIN_COUNT:
            activeTime[trackDate] += 5
            activeIndex[trackDate] += movement 

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
        t1ValDict['value'] = sedentaryTime[trackDate] 
        t1Dict['data'] = t1ValDict
        t1.append(t1Dict)
        if (sedentaryTime[trackDate] > t1Max): t1Max = sedentaryTime[trackDate]
        if (sedentaryTime[trackDate] < t1Min): t1Min = sedentaryTime[trackDate] 
        
        t2Dict = dict()
        t2ValDict = dict()
        t2ValDict['name'] = trackDate
        t2ValDict['value'] = sedentaryIndex[trackDate]
        t2Dict['data'] = t2ValDict
        t2.append(t2Dict)
        if (sedentaryIndex[trackDate] > t2Max): t2Max = sedentaryIndex[trackDate]
        if (sedentaryIndex[trackDate] < t2Min): t2Min = sedentaryIndex[trackDate]
        
        t3Dict = dict()
        t3ValDict = dict()
        t3ValDict['name'] = trackDate
        t3ValDict['value'] = activeTime[trackDate]
        t3Dict['data'] = t3ValDict 
        t3.append(t3Dict)
        if (activeTime[trackDate] > t3Max): t3Max = activeTime[trackDate]
        if (activeTime[trackDate] < t3Min): t3Min = activeTime[trackDate]
        
        t4Dict = dict()
        t4ValDict = dict()
        t4ValDict['name'] = trackDate
        t4ValDict['value'] = activeIndex[trackDate]
        t4Dict['data'] = t4ValDict 
        t4.append(t4Dict)
        if (activeIndex[trackDate] > t4Max): t4Max = activeIndex[trackDate]
        if (activeIndex[trackDate] < t4Min): t4Min = activeIndex[trackDate] 
    mobility = dict()
    """
    mobility['sedentary_time'] = dict() 
    mobility['sedentary_time']['data'] = t1
    mobility['sedentary_time']['title'] = "Sedentary Time"
    mobility['sedentary_time']['y_suffix'] = "minute(s)"
    mobility['sedentary_time']['y_min'] = t1Min
    mobility['sedentary_time']['y_max'] = t1Max 
    
    mobility['sedentary_index'] = dict()
    mobility['sedentary_index']['data'] = t2 
    mobility['sedentary_index']['title'] = "Sedentary Index"
    mobility['sedentary_index']['y_suffix'] = ""
    mobility['sedentary_index']['y_min'] = t2Min
    mobility['sedentary_index']['y_max'] = t2Max
    """
    
    mobility['time'] = dict() 
    mobility['time']['data'] = t3
    mobility['time']['title'] = "Active Time"
    mobility['time']['y_suffix'] = "minutes(s)"
    mobility['time']['y_min'] = t3Min
    mobility['time']['y_max'] = t3Max 
    
    mobility['index'] = dict() 
    mobility['index']['data'] = t4
    mobility['index']['title'] = "Active Index"
    mobility['index']['y_suffix'] = ""
    mobility['index']['y_min'] = t4Min
    mobility['index']['y_max'] = t4Max
    
    return mobility






