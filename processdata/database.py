import sqlite3
import sys 
import os

import numpy as np 

from instance import SensingData, SleepLog, SysEvent, MovementRawData,\
    SoundRawData, LightRawData, ProximityRawData, LifestyleRawData 

class DatabaseHelper():
    """
    The database class that used to access a sqlite3 database file. It contains all
    necessary functions that used in the project. 
    """
    
    def __init__(self, fullDBPath):
        self.fullDBPath = fullDBPath
        self.con = None
        
        if not os.path.exists(self.fullDBPath):
            print self.fullDBPath 
            print "The path of database file is not correct, please double check the file path ==================."
            sys.exit(1) 
        
        try:
            # http://stackoverflow.com/questions/1829872/read-datetime-back-from-sqlite-as-a-datetime-in-python 
            self.con = sqlite3.connect(self.fullDBPath, detect_types = sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        except sqlite3.Error, e:
            print "Connect to database %s error: %s" % (self.fullDBPath, e.args[0])
            sys.exit(1)
    
    def __del__(self):
        if self.con != None:
            self.con.close()
    
    def getSensingData(self):
        data = []
        sqlstr = "SELECT createTime as \"[timestamp]\", trackDate, movement, illuminanceMax, illuminanceMin, illuminanceAvg, illuminanceStd, \
                    decibelMax, decibelMin, decibelAvg, decibelStd, isCharging, powerLevel, proximity, ssid, appUsage \
                    FROM sensingdata" 
        try:
            cur = self.con.cursor()
            cur.execute(sqlstr)
            rows = cur.fetchall()
            
            for row in rows:
                createTime = row[0]
                trackDate = row[1]
                movement = int(row[2]) 
                illuminanceMax = float(row[3])
                illuminanceMin = float(row[4])
                illuminanceAvg = float(row[5])
                illuminanceStd = float(row[6])
                decibelMax = float(row[7])
                decibelMin = float(row[8])
                decibelAvg = float(row[9])
                decibelStd = float(row[10])
                isCharging = int(row[11]) 
                powerLevel = float(row[12])
                proximity = float(row[13]) 
                ssid = row[14]
                appUsage = row[15]
                oneRecord = SensingData(createTime, trackDate, movement, illuminanceMax, illuminanceMin, illuminanceAvg, illuminanceStd,
                         decibelMax, decibelMin, decibelAvg, decibelStd, isCharging, powerLevel, proximity, ssid, appUsage, 0)
                data.append(oneRecord) 
        except sqlite3.Error, e:
            print "Query sensingdata table error: %s" % (e.args[0])
            sys.exit(1)
        finally:
            cur.close()
        return data    
    
    def getSleepLog(self):
        """
        Pull all sleep log from database to a list. We need to sort the record by sleep time
        since we will use this time stamp to combine the raw data. 
        """
        data = []
        sqlstr = "SELECT createTime as \"[timestamp]\", trackDate, sleepTime as \"[timestamp]\", \
                    wakeupTime as \"[timestamp]\", napTime, quality, finished FROM sleeplogger \
                    order by date(sleepTime) ASC "
        
        try:
            cur = self.con.cursor()
            cur.execute(sqlstr)
            rows = cur.fetchall()
            
            for row in rows:
                createTime = row[0]
                trackDate = row[1]
                sleepTime = row[2]
                wakeupTime = row[3]
                napTime = int(row[4])
                quality = int(row[5])
                finished = int(row[6])
                oneRecord = SleepLog(createTime, trackDate, sleepTime, wakeupTime, napTime, quality, finished)
                data.append(oneRecord)
            return data 
        except sqlite3.Error, e:
            print "Query sleeplogger table error: %s" % (e.args[0])
            sys.exit(1)
        finally:
            cur.close()
    
    def getSystemEvents(self):
        data = []
        sqlstr = "SELECT createTime as \"[timestamp]\", trackDate, eventType FROM sysevents"
        
        try:
            cur = self.con.cursor()
            cur.execute(sqlstr)
            rows = cur.fetchall()
            
            for row in rows:
                createTime = row[0]
                trackDate = row[1]
                eventType = int(row[2])
                oneRecord = SysEvent(createTime, trackDate, eventType)
                data.append(oneRecord)
            return data
        except sqlite3.Error, e:
            print "Query sysevents table error: %s" % (e.args[0])
            sys.exit(1)
        finally:
            cur.close()
    
    def getMovmentRaw(self):
        ret = [] 
        sqlstr = "SELECT createTime as \"[timestamp]\", data FROM movementraw" 
        
        try:
            cur = self.con.cursor()
            cur.execute(sqlstr)
            rows = cur.fetchall() 
            
            for row in rows:
                createTime = row[0]
                data = row[1]
                oneRecord = MovementRawData(createTime, data)
                ret.append(oneRecord)
            return ret
        except sqlite3.Error, e:
            print "Query movementraw table error: %s" % (e.args[0])
            sys.exit(1)
        finally:
            cur.close()
        
    def getSoundRaw(self):
        ret = [] 
        sqlstr = "SELECT createTime as \"[timestamp]\", data FROM soundraw" 
        
        try:
            cur = self.con.cursor()
            cur.execute(sqlstr)
            rows = cur.fetchall() 
            
            for row in rows:
                createTime = row[0]
                data = row[1]
                oneRecord = SoundRawData(createTime, data)
                ret.append(oneRecord)
            return ret
        except sqlite3.Error, e:
            print "Query soundraw table error: %s" % (e.args[0])
            sys.exit(1)
        finally:
            cur.close()

    def getLightRaw(self):
        ret = [] 
        sqlstr = "SELECT createTime as \"[timestamp]\", data FROM lightraw" 
        
        try:
            cur = self.con.cursor()
            cur.execute(sqlstr)
            rows = cur.fetchall() 
            
            for row in rows:
                createTime = row[0]
                data = row[1]
                oneRecord = LightRawData(createTime, data)
                ret.append(oneRecord)
            return ret
        except sqlite3.Error, e:
            print "Query lightraw table error: %s" % (e.args[0])
            sys.exit(1)
        finally:
            cur.close()
    
    def getProximityRaw(self):
        ret = [] 
        sqlstr = "SELECT createTime as \"[timestamp]\", data FROM proximityraw" 
        
        try:
            cur = self.con.cursor()
            cur.execute(sqlstr)
            rows = cur.fetchall() 
            
            for row in rows:
                createTime = row[0]
                data = row[1]
                oneRecord = ProximityRawData(createTime, data)
                ret.append(oneRecord)
            return ret
        except sqlite3.Error, e:
            print "Query proximityraw table error: %s" % (e.args[0])
            sys.exit(1)
        finally:
            cur.close()

    def getLifestyleRaw(self):
        ret = []
        sqlstr = "SELECT trackDate, createTime as \"[timestamp]\", type, typeId, logTime as \"[timestamp]\", selection, note FROM lifestyleraw"
        
        try:
            cur = self.con.cursor()
            cur.execute(sqlstr)
            rows = cur.fetchall() 
            
            for row in rows:
                trackDate = row[0]
                createTime = row[1]
                typeName = row[2]
                typeId = int(row[3])
                logTime = row[4]
                selection = row[5]
                note = row[6] 
                oneRecord = LifestyleRawData(trackDate, createTime, typeName, typeId, logTime, selection, note)
                ret.append(oneRecord)
            return ret
        except sqlite3.Error, e:
            print "Sqlite Query lifestyleraw table error: %s" % (e)
            sys.exit(1)
        finally:
            cur.close()



if __name__ == "__main__":
    test = DatabaseHelper("./data/6e44881f5af5d54a452b99f57899a7.db")
    """
    data1 = test.getSensingData()
    data2 = test.getSleepLog()
    data3 = test.getSystemEvents()
    print data1[0]
    print "\n\n" 
    print data2[0] 
    print "\n\n"
    print data3[0] 
    """
    data = test.getIlluminanceSTD()
    print data 
    
    
    