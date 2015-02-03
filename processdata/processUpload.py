from database import DatabaseHelper
from mysqlHelper import MysqlHelper
from glob import glob 

import zipfile, os.path 
import shutil 
import json
from constants import DONE_FILE_DIR, RAW_FILE_DIR
from instance import *
from roomDetector import RoomDetector
from datetime import datetime
from sleepEngine import SleepEngine

def unzipFile(sourceFile): 
    dest_dir = os.path.dirname(sourceFile)
    fileName = os.path.basename(sourceFile).split(".zip")[0]
    dbFilePath = os.path.join(dest_dir, fileName + ".db") 
    
    with zipfile.ZipFile(sourceFile, "r", zipfile.ZIP_STORED) as zf:
        zf.extractall(dest_dir)
    return dbFilePath  

def storeDataIntoMysql(sourceFile, cid):
    """
    The bedtime and waketime will be calculated on server. User will
    download the bedtime/waketime periodically and if the time is updated
    by user, the new time will be uploaded to server as well. We do not
    need to copy the sleeplog data from the uploaded database file. 
    """
    
    sqliteDB     = DatabaseHelper(sourceFile) 
    sensingData  = sqliteDB.getSensingData() 
    #sleepData    = sqliteDB.getSleepLog()
    syseventData = sqliteDB.getSystemEvents()
    movementRaw  = sqliteDB.getMovmentRaw()
    soundRaw     = sqliteDB.getSoundRaw()
    lightRaw     = sqliteDB.getLightRaw()
    proximityRaw = sqliteDB.getProximityRaw()
    lifestyleRaw = sqliteDB.getLifestyleRaw() 
    
    mysqlDB = MysqlHelper()
    mysqlDB.insertSensingDataList(sensingData, cid)
    #mysqlDB.insertSleepDataList(sleepData, cid)
    mysqlDB.insertSysEventDataList(syseventData, cid)
    mysqlDB.insertMovementDataList(movementRaw, cid)
    mysqlDB.insertSoundDataList(soundRaw, cid)
    mysqlDB.insertLightDataList(lightRaw, cid)
    mysqlDB.insertProximityDataList(proximityRaw, cid) 
    mysqlDB.insertLifestyleDataList(lifestyleRaw, cid)
    
def cleanUp(zipFile, dbFile, dest_dir):
    zipBaseName = os.path.basename(zipFile)
    dbBaseName  = os.path.basename(dbFile)
    os.rename(zipFile, os.path.join(dest_dir, zipBaseName))
    os.rename(dbFile, os.path.join(dest_dir, dbBaseName)) 

def processUnhandledFiles(uuid, cid):
    mysqlHelper = MysqlHelper()
    if not mysqlHelper.checkUserExists(cid, uuid):
        mysqlHelper.insertUser(cid, uuid) 
    
    fileList = glob(RAW_FILE_DIR + "*.txt")
    for idx in range(len(fileList)):
        filePath = fileList[idx]
        print "Processing file: " + filePath 
        fileName = os.path.basename(filePath)
        uuid = fileName.split('_')[0]
        cid = mysqlHelper.getCidByUuid(uuid) 
        processSyncData(filePath, cid, uuid) 

def processUploadedFile(sourceFile, cid, uuid):
    mysqlDB = MysqlHelper()
    if not mysqlDB.checkUserExists(cid, uuid):
        mysqlDB.insertUser(cid, uuid) 
    
    # Unzip the uploaded database file 
    dbFilePath = unzipFile(sourceFile) 
    
    # Read from SqLite database and store the data into MySQL database
    storeDataIntoMysql(dbFilePath, cid)
    
    # Clean up, move the processed files into done folder 
    cleanUp(sourceFile, dbFilePath, DONE_FILE_DIR) 
    
def processSyncData(filePath, cid, uuid): 
    with open(filePath) as jsonFile:
        data = json.load(jsonFile) 
    
    mysqlHelper = MysqlHelper()
    """
    if not mysqlHelper.checkUserExists(cid, uuid):
        mysqlHelper.insertUser(cid, uuid) 
    """

    lastSensingdataTS = None

    if "sleepLog" in data:
        sleepLogData = data['sleepLog']
        for oneItem in sleepLogData:
            exists = mysqlHelper.checkSleepLogExists(cid, oneItem['trackDate'])
            oneRecord = SleepLog(datetime.strptime(oneItem['createTime'], '%m/%d/%Y %H:%M:%S'), \
                            oneItem['trackDate'], datetime.strptime(oneItem['sleepTime'], '%m/%d/%Y %H:%M:%S'), \
                            datetime.strptime(oneItem['wakeupTime'], '%m/%d/%Y %H:%M:%S'), oneItem['napTime'], 0, 1)
            if exists:
                mysqlHelper.updateSleepLogData(oneRecord, cid)
            else:
                mysqlHelper.insertSleepData(oneRecord, cid)
    
    if "dailyLog" in data:
        dailyLogData = data["dailyLog"]
        for oneItem in dailyLogData:
            exists = mysqlHelper.checkDailyLogExists(cid, oneItem['trackDate']) 
            oneRecord = DailyLogData(oneItem['trackDate'], datetime.strptime(oneItem['createTime'], '%m/%d/%Y %H:%M:%S'), \
                            oneItem['numAwakenings'], oneItem['timeAwake'],\
                            oneItem['timeToSleep'], oneItem['quality'], oneItem['restored'], oneItem['stress'], \
                            oneItem['depression'], oneItem['fatigue'], oneItem['sleepiness']) 
            if exists:
                mysqlHelper.updateDailyLogData(oneRecord, cid, oneItem['trackDate']) 
            else:
                mysqlHelper.insertDailyLogData(oneRecord, cid) 
    
    if "lifestyleRaw" in data:
        lifestyleData = data["lifestyleRaw"]
        for oneItem in lifestyleData:
            oneRecord = LifestyleRawData(oneItem['trackDate'], datetime.strptime(oneItem['createTime'], '%m/%d/%Y %H:%M:%S'), \
                            oneItem['typeName'], int(oneItem['typeId']), datetime.strptime(oneItem['logTime'], '%m/%d/%Y %H:%M:%S'), \
                            int(oneItem['selection']), oneItem['note'])
            mysqlHelper.insertLifestyleRawData(oneRecord, cid)
    
    if "lightRaw" in data:
        lightData = data["lightRaw"]
        for oneItem in lightData:
            oneRecord = LightRawData(datetime.strptime(oneItem['createTime'], '%m/%d/%Y %H:%M:%S'), oneItem['data'])
            mysqlHelper.insertLightData(oneRecord, cid)
        
    if "movementRaw" in data:
        movementData = data['movementRaw']
        for oneItem in movementData:
            oneRecord = MovementRawData(datetime.strptime(oneItem['createTime'], '%m/%d/%Y %H:%M:%S'), oneItem['data'])
            mysqlHelper.insertMovementData(oneRecord, cid)
        
    if "proximityRaw" in data:
        proximityData = data['proximityRaw']
        for oneItem in proximityData:
            oneRecord = ProximityRawData(datetime.strptime(oneItem['createTime'], '%m/%d/%Y %H:%M:%S'), oneItem['data'])
            mysqlHelper.insertProximityData(oneRecord, cid)
    
    if "sensingData" in data:
        roomDetector = RoomDetector(cid, mysqlHelper) 
        
        sensing = data['sensingData']
        for oneItem in sensing:
            oneRecord = SensingData(datetime.strptime(oneItem['createTime'], '%m/%d/%Y %H:%M:%S'), oneItem['trackDate'], int(oneItem['movement']), \
                            float(oneItem['illuminanceMax']), float(oneItem['illuminanceMin']), float(oneItem['illuminanceAvg']), float(oneItem['illuminanceStd']), \
                            float(oneItem['decibelMax']), float(oneItem['decibelMin']), float(oneItem['decibelAvg']), float(oneItem['decibelStd']), \
                            int(oneItem['isCharging']), float(oneItem['powerLevel']), float(oneItem['proximity']), oneItem['ssid'], oneItem['appUsage'], 0)
            mysqlHelper.insertSensingData(oneRecord, cid, roomDetector)
        lastSensingdataTS = datetime.strptime(sensing[-1]['createTime'], '%m/%d/%Y %H:%M:%S')
    
    if "soundRaw" in data:
        soundData = data['soundRaw']
        for oneItem in soundData:
            oneRecord = SoundRawData(datetime.strptime(oneItem['createTime'], '%m/%d/%Y %H:%M:%S'), oneItem['data'])
            mysqlHelper.insertSoundData(oneRecord, cid)
    
    if "sysEvents" in data:
        eventData = data['sysEvents']
        for oneItem in eventData:
            oneRecord = SysEvent(datetime.strptime(oneItem['createTime'], '%m/%d/%Y %H:%M:%S'), oneItem['trackDate'], int(oneItem['eventType']))
            mysqlHelper.insertSysEventData(oneRecord, cid)
    
    # Calculate the sleep time and wakeup time, this need to be done in another thread
    engine = SleepEngine(cid, lastSensingdataTS)
    engine.calculateSleep()

def processUploadSurvey(uuid, cid, age, gender, racial, sleepHours): 
    mysqlHelper = MysqlHelper()
    if not mysqlHelper.checkUserExists(cid, uuid):
        mysqlHelper.insertUser(cid, uuid, age, gender, racial, sleepHours) 
    else:
        mysqlHelper.updateUser(cid, uuid, age, gender, racial, sleepHours)

    
    

if __name__ == "__main__":
    #unzipFile("/home/ke/Desktop/658ac828bdadbddaa909315ad80ac8.zip")
    #processUploadedFile("/home/ke/sleepfit/doneFile/6e44881f5af5d54a452b99f57899a7_201412032117.zip", "6e44881f5af5d54a452b99f57899a7", "6e44881f5af5d54a452b99f57899a7")
    #processSyncData("{\"soundRaw\":[{\"data\":\"43|40|50|67|50|39|38|69|65|42\",\"id\":\"1\",\"createTime\":\"12\/22\/2014 10:54:30\"}]}", "6e44881f5af5d54a452b99f57899a7", "6e44881f5af5d54a452b99f57899a7") 
    processSyncData("/home/ke/sleepfit/rawFile/6e44881f5af5d54a452b99f57899a7_201501041301.txt", "6e44881f5af5d54a452b99f57899a7", "6e44881f5af5d54a452b99f57899a7")
    #processUnhandledFiles("6e44881f5af5d54a452b99f57899a7", "6e44881f5af5d54a452b99f57899a7")
    
