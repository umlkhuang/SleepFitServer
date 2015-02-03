import MySQLdb 
import sys

from datetime import datetime 
from constants import MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB

from instance import SensingData, SleepLog, SysEvent, MovementRawData,\
    SoundRawData, LightRawData, ProximityRawData, RoomData, LifestyleRawData
from roomDetector import RoomDetector
    
class MysqlHelper(object):
    def __init__(self):
        self.db = None
        try:
            self.db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
        except MySQLdb.Error, e:
            print "Connect to SQL database sleepfit error: %s" % (e)
            sys.exit(1)
    
    def __del__(self):
        if self.db is not None:
            self.db.close() 
    
    def insertSensingData(self, sensingData, cid, roomDetector): 
        roomId = roomDetector.getRoomIdBySsid(sensingData.ssid) 
        success = False 
        
        sql = "INSERT INTO sensingdata (CID, createTime, trackDate, movement, illuminanceMax, illuminanceMin, illuminanceAvg, illuminanceStd, \
                decibelMax, decibelMin, decibelAvg, decibelStd, isCharging, powerLevel, proximity, ssid, appUsage, roomId) \
                VALUES ('%s', '%s', '%s', '%d', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%d', '%f', '%f', '%s', '%s', '%s')" % \
                (cid, sensingData.createTime, sensingData.trackDate, sensingData.movement, sensingData.illuminanceMax, sensingData.illuminanceMin, \
                 sensingData.illuminanceAvg, sensingData.illuminanceStd, sensingData.decibelMax, sensingData.decibelMin, sensingData.decibelAvg, \
                 sensingData.decibelStd, sensingData.isCharging, sensingData.powerLevel, sensingData.proximity, sensingData.ssid, sensingData.appUsage, roomId)
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit() 
            success = True 
        except MySQLdb.Error, e:
            print "Insert into table sensingdata error: %s" % (e)  
            self.db.rollback() 
            success = False
        finally:
            cursor.close() 
            return success 
    
    def insertSensingDataList(self, dataList, cid):
        roomDetector = RoomDetector(cid, self) 
        for sensingData in dataList:
            self.insertSensingData(sensingData, cid, roomDetector)
    
    def insertSleepData(self, sleepData, cid):
        success = False
        
        sql = "INSERT INTO sleeplogger (CID, createTime, trackDate, sleepTime, wakeupTime, napTime, quality, finished) \
                VALUES ('%s', '%s', '%s', '%s', '%s', '%d', '%d')" % \
                (cid, sleepData.createTime, sleepData.trackDate, sleepData.sleepTime, sleepData.wakeupTime, sleepData.napTime, sleepData.quality, sleepData.finished)
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit() 
            success = True
        except MySQLdb.Error, e:
            print "Insert into table sleeplogger error: %s" % (e)  
            self.db.rollback() 
            success = False
        finally:
            cursor.close() 
            return success 

    def insertSleepDataList(self, dataList, cid):
        for sleepData in dataList:
            self.insertSleepData(sleepData, cid)

    def checkSleepLogExists(self, cid, trackDate):
        sql = "SELECT * from sleeplogger WHERE CID = '%s' AND trackDate = '%s'" % (cid, trackDate)
        exists = False
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                exists = True
            else:
                exists = False
        except MySQLdb.Error, e:
            exists = False
            print "Query table sleeplogger error: %s" % (e)
        finally:
            cursor.close()
            return exists

    def checkUserUpdatedSleep(self, cid, trackDate):
        sql = "SELECT * from sleeplogger WHERE CID = '%s' AND trackDate = '%s' AND finished = '%d'" % (cid, trackDate, 1)
        exists = False
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                exists = True
            else:
                exists = False
        except MySQLdb.Error, e:
            exists = False
            print "Query table sleeplogger error: %s" % (e)
        finally:
            cursor.close()
            return exists

    def updateSleepLogData(self, sleepData, cid):
        success = False

        sql = "UPDATE sleeplogger SET sleepTime = '%s', wakeupTime = '%s', napTime = '%d', finished = '%d'\
                WHERE CID = '%s' AND trackDate = '%s'" % (sleepData.sleepTime, sleepData.wakeupTime, sleepData.napTime, sleepData.finished, \
                cid, sleepData.trackDate)
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            success = True
        except MySQLdb.Error, e:
            print "Update table sleeplogger error: %s" % (e)
            self.db.rollback()
            success = False
        finally:
            cursor.close()
            return success
    
    def insertSysEventData(self, sysevent, cid):
        success = False
        
        sql = "INSERT INTO sysevents (CID, createTime, trackDate, eventType) \
                VALUES ('%s', '%s', '%s', '%d')" % \
                (cid, sysevent.createTime, sysevent.trackDate, sysevent.eventType) 
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit() 
            success = True 
        except MySQLdb.Error, e:
            print "Insert into table sysevents error: %s" % (e)  
            self.db.rollback() 
            success = False 
        finally:
            cursor.close() 
            return success 
    
    def insertSysEventDataList(self, dataList, cid):
        for sysevent in dataList:
            self.insertSysEventData(sysevent, cid)
    
    def insertMovementData(self, movementData, cid): 
        success = False
        
        sql = "INSERT INTO movementraw (CID, createTime, data) \
                VALUES ('%s', '%s', '%s')" % (cid, movementData.createTime, movementData.data) 
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit() 
            success = True
        except MySQLdb.Error, e:
            print "Insert into table movementraw error: %s" % (e)  
            self.db.rollback() 
            success = False
        finally:
            cursor.close() 
            return success 
    
    def insertMovementDataList(self, movementList, cid):
        for movementData in movementList:
            self.insertMovementData(movementData, cid)
    
    def insertSoundData(self, soundData, cid): 
        success = False
        
        sql = "INSERT INTO soundraw (CID, createTime, data) \
                VALUES ('%s', '%s', '%s')" % (cid, soundData.createTime, soundData.data) 
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit() 
            success = True 
        except MySQLdb.Error, e:
            print "Insert into table soundraw error: %s" % (e)  
            self.db.rollback() 
            success = False
        finally:
            cursor.close() 
            return success 
    
    def insertSoundDataList(self, soundList, cid):
        for soundData in soundList:
            self.insertSoundData(soundData, cid)
            
    def insertLightData(self, lightData, cid): 
        success = False 
        
        sql = "INSERT INTO lightraw (CID, createTime, data) \
                VALUES ('%s', '%s', '%s')" % (cid, lightData.createTime, lightData.data) 
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit() 
            success = True
        except MySQLdb.Error, e:
            print "Insert into table lightraw error: %s" % (e)  
            self.db.rollback() 
            success = False 
        finally:
            cursor.close() 
            return success
    
    def insertLightDataList(self, lightList, cid):
        for lightData in lightList:
            self.insertLightData(lightData, cid)

    def insertProximityData(self, proximityData, cid): 
        success = False
        
        sql = "INSERT INTO proximityraw (CID, createTime, data) \
                VALUES ('%s', '%s', '%s')" % (cid, proximityData.createTime, proximityData.data) 
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit() 
            success = True
        except MySQLdb.Error, e:
            print "Insert into table proximityraw error: %s" % (e.args[0])  
            self.db.rollback() 
            success = False
        finally:
            cursor.close() 
            return success 
    
    def insertProximityDataList(self, proximityList, cid):
        for proximityData in proximityList:
            self.insertProximityData(proximityData, cid)

    def insertDailyLogData(self, dailyLogData, cid):
        success = False
        
        sql = "INSERT INTO dailylog (CID, trackDate, createTime, numAwakenings, timeAwake, timeToSleep, quality, restored, stress, \
                depression, fatigue, sleepiness) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                % (cid, dailyLogData.trackDate, dailyLogData.createTime, dailyLogData.numAwakenings, dailyLogData.timeAwake, \
                   dailyLogData.timeToSleep, dailyLogData.quality, dailyLogData.restored, dailyLogData.stress, \
                   dailyLogData.depression, dailyLogData.fatigue, dailyLogData.sleepiness) 
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit() 
            success = True
        except MySQLdb.Error, e:
            print "Insert into table dailylog error: %s" % (e)  
            self.db.rollback() 
            success = False
        finally:
            cursor.close()
            return success
    
    def insertDailyLogDataList(self, dailyLogList, cid): 
        for dailyLogData in dailyLogList:
            self.insertDailyLogData(dailyLogData, cid) 
    
    def updateDailyLogData(self, dailyLogData, cid, trackDate): 
        success = False
        
        sql = "UPDATE dailylog SET numAwakenings = '%s', timeAwake = '%s', timeToSleep = '%s', quality = '%s', restored = '%s', \
                stress = '%s', depression = '%s', fatigue = '%s', sleepiness = '%s' WHERE CID = '%s' AND trackDate = '%s'" % (dailyLogData.numAwakenings, \
                dailyLogData.timeAwake, dailyLogData.timeToSleep, dailyLogData.quality, dailyLogData.restored, \
                dailyLogData.stress, dailyLogData.depression, dailyLogData.fatigue, dailyLogData.sleepiness, cid, trackDate)  
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit() 
            success = True
        except MySQLdb.Error, e:
            print "Update table dailylog error: %s" % (e)  
            self.db.rollback() 
            success = False
        finally:
            cursor.close() 
            return success 
    
    def checkDailyLogExists(self, cid, trackDate):
        sql = "SELECT * from dailylog WHERE CID = '%s' AND trackDate = '%s'" % (cid, trackDate)
        exists = False 
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                exists = True 
            else:
                exists = False 
        except MySQLdb.Error, e: 
            exists = False
            print "Query table dailylog error: %s" % (e) 
        finally:
            cursor.close()
            return exists 

    def insertLifestyleRawData(self, lifestyleData, cid):
        success = False
        
        sql = "INSERT INTO lifestyleraw (CID, trackDate, createTime, type, typeId, logTime, selection, note) \
                VALUES ('%s', '%s', '%s', '%s', '%d', '%s', '%d', '%s')" \
                % (cid, lifestyleData.trackDate, lifestyleData.createTime, lifestyleData.typeName, \
                   lifestyleData.typeId, lifestyleData.logTime, lifestyleData.selection, lifestyleData.note)
        
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit() 
            success = True
        except MySQLdb.Error, e:
            print "Insert into table lifestyleraw error: %s" % (e)  
            self.db.rollback() 
            success = False
        finally:
            cursor.close()
            return success
            
    def insertLifestyleDataList(self, lifestyleList, cid):
        for lifestyleData in lifestyleList:
            self.insertLifestyleRawData(lifestyleData, cid) 

    def insertUser(self, cid, uuid, age, gender, racial, sleepHours): 
        success = False
        
        sql = "INSERT INTO users (CID, UUID, age, gender, racial, sleepHours) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" \
                    % (cid, uuid, age, gender, racial, sleepHours) 
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit() 
            success = True
        except MySQLdb.Error, e:
            print "Insert into table users error: %s" % (e)  
            self.db.rollback() 
            success = False
        finally:
            cursor.close() 
            return success 
    
    def updateUser(self, cid, uuid, age, gender, racial, sleepHours):
        success = False
        
        sql = "UPDATE users SET age = '%s', gender = '%s', racial = '%s', sleepHours = '%s' WHERE CID = '%s' AND UUID = '%s'" \
                    % (age, gender, racial, sleepHours, cid, uuid)         
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit() 
            success = True
        except MySQLdb.Error, e:
            print "Update table users error: %s" % (e)  
            self.db.rollback() 
            success = False
        finally:
            cursor.close() 
            return success 
    
    def getSensingDataByTime(self, fromTS, toTS, cid):
        data = list()
        
        sql = "SELECT createTime as \"[timestamp]\", trackDate, movement, illuminanceMax, illuminanceMin, illuminanceAvg, illuminanceStd, \
                decibelMax, decibelMin, decibelAvg, decibelStd, isCharging, powerLevel, proximity, ssid, appUsage, roomId \
                FROM sensingdata WHERE CID = '%s' AND createTime >= '%s' AND createTime <= '%s' \
                ORDER BY createTime ASC " % (cid, fromTS, toTS)
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
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
                roomId = int(row[16]) 
                oneRecord = SensingData(createTime, trackDate, movement, illuminanceMax, illuminanceMin, illuminanceAvg, illuminanceStd,
                         decibelMax, decibelMin, decibelAvg, decibelStd, isCharging, powerLevel, proximity, ssid, appUsage, roomId)
                data.append(oneRecord) 
        except MySQLdb.Error, e:
            print "Query table sensingdata error: %s" % (e) 
        finally:
            cursor.close() 
            return data 

    def getSensingDataByUser(self, cid):
        data = list()
        
        sql = "SELECT createTime as \"[timestamp]\", trackDate, movement, illuminanceMax, illuminanceMin, illuminanceAvg, illuminanceStd, \
                decibelMax, decibelMin, decibelAvg, decibelStd, isCharging, powerLevel, proximity, ssid, appUsage, roomId \
                FROM sensingdata WHERE CID = '%s' ORDER BY createTime ASC " % (cid) 
        
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall() 
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
                roomId = int(row[16])
                oneRecord = SensingData(createTime, trackDate, movement, illuminanceMax, illuminanceMin, illuminanceAvg, illuminanceStd,
                         decibelMax, decibelMin, decibelAvg, decibelStd, isCharging, powerLevel, proximity, ssid, appUsage, roomId)
                data.append(oneRecord) 
        except MySQLdb.Error, e:
            print "Query table sensingdata error: %s" % (e) 
        finally:
            cursor.close() 
            return data  
        
    def getLifestyleData(self, cid, trackDate):
        data = list()
        
        sql = "SELECT createTime as \"[timestamp]\", type, typeId, logTime as \"[timestamp]\", \
                selection, note FROM lifestyleraw WHERE trackDate = '%s' AND cid = '%s' ORDER BY logTime DESC" \
                % (trackDate, cid)
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall() 
            for row in rows:
                createTime = row[0]
                typeName = row[1]
                typeId = int(row[2])
                logTime = row[3]
                selection = row[4]
                note = row[5]
                oneRecord = LifestyleRawData(trackDate, createTime, typeName, typeId, logTime, selection, note)
                data.append(oneRecord) 
        except MySQLdb.Error, e:
            print "Query table lifestyleraw error: %s" % (e) 
        finally:
            cursor.close() 
        return data

    def getSleepLogData(self, cid, trackDate):
        data = list()

        sql = "SELECT sleepTime as \"[timestamp]\", wakeupTime as \"[timestamp]\" FROM sleeplogger \
              WHERE CID = '%s' AND trackDate = '%s' " % (cid, trackDate)

        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                sleepTime = row[0]
                wakeupTime = row[1]
                oneRecord = SleepLog(0, trackDate, sleepTime, wakeupTime, 0, 0)
                data.append(oneRecord)
        except MySQLdb.Error, e:
            print "Query table sleeplogger error: %s" % (e)
        finally:
            cursor.close()
        return data

    def checkUserExists(self, cid, uuid):
        sql = "SELECT * from users WHERE CID = '%s' AND UUID = '%s'" % (cid, uuid)
        exists = False 
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                exists = True 
            else:
                exists = False 
        except MySQLdb.Error, e: 
            exists = False
            print "Query table users error: %s" % (e) 
        finally:
            cursor.close()
            return exists 
        
    def getCidByUuid(self, uuid):
        sql = "SELECT CID from users WHERE UUID = '%s'" % (uuid)
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) <= 0:
                return ""
            elif len(rows) > 1:
                print "Duplicated UUID for different user!"
                return "" 
            else:
                return rows[0][0] 
        except MySQLdb.Error, e:
            print "Query table users error: %s" % (e) 
            return "" 
        finally:
            cursor.close()

    def getRoomInfoByUser(self, cid):
        data = list() 
        
        sql = "SELECT ID, wifi FROM rooms WHERE CID = '%s'" % (cid)
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall() 
            for row in rows:
                oneRecord = RoomData(row[0], row[1])
                data.append(oneRecord)
        except MySQLdb.Error, e:
            print "Query table rooms error: %s" % (e) 
        finally:
            cursor.close() 
            return data 

    def insertNewRoom(self, cid, wifi):
        sql = "INSERT INTO rooms (CID, wifi) VALUES ('%s', '%s')" % (cid, wifi) 
        roomId = -1 
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit() 
            roomId = cursor.lastrowid 
        except MySQLdb.Error, e:
            print "Insert into table rooms error: %s" % (e)  
            self.db.rollback() 
        finally:
            cursor.close() 
            return roomId 



if __name__ == "__main__":
    entry = SensingData(datetime.now(), "11/02/2014", 1232, 231.1, 12.22, 122.43, 12.4, 45, 34.3, 40.4, 3.8, 1, 0.97, 2.5, "adfasfdsaf", "adsfasfdsafadf")
    a = MysqlHelper()
    a.insertSensingData(entry, "adfafdsf") 
    ret = a.getSensingDataByTime(datetime(2014,11,02,10,01,00), datetime(2014,11,03,22,27,00), "adfafdsf")
    for data in ret:
        print data
    
        