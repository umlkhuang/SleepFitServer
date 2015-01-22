from util import Counter
from math import sqrt 
from instance import RoomData
from constants import ROOM_SIMILARITY_THRESHOLD#, MYSQL_DB, MYSQL_HOST, MYSQL_PASS, MYSQL_USER 

import itertools
import operator 
import sys
import MySQLdb 

class RoomDetector(object):
    def __init__(self, cid, mysqlHelper):
        self.cid = cid 
        self.mysqlHelper = mysqlHelper 
        self.db = mysqlHelper.db 
        # The returned rooms is a dictionary 
        self.rooms = self.pullRoomsInfo(self.cid)
        
    def pullRoomsInfo(self, cid):
        roomData = list() 
        
        sql = "SELECT ID, wifi FROM rooms WHERE CID = '%s'" % (cid)
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall() 
            for row in rows:
                oneRecord = RoomData(int(row[0]), row[1])
                roomData.append(oneRecord)
        except MySQLdb.Error, e:
            print "Query table rooms error: %s" % (e) 
        finally:
            return roomData 
    
    def parseWifiRaw2Counter(self, wifiRawStr):
        wifiCounter = Counter()
        if wifiRawStr != "":
            wifiList = wifiRawStr.split(", ")
            for oneWifi in wifiList: 
                tmp = oneWifi.split("#") 
                if len(tmp) == 2:
                    wifiCounter[tmp[0]] = int(tmp[1]) 
                else:
                    continue 
        return wifiCounter 
    
    def getCosineSimilarity(self, counter1, counter2):
        """
        Calculate the Cosine similarity between two counters 
        """
        product = counter1 * counter2 * 1.0 
        mag1 = sqrt(counter1 * counter1) 
        mag2 = sqrt(counter2 * counter2) 
        if mag1 == 0.0 or mag2 == 0.0:
            similarity = 0.0 
        else:
            similarity = product / (mag1 * mag2) 
        return similarity 
    
    def getTanimotoSimilarity(self, counter1, counter2):
        """
        Calculate the Tanimoto similarity between two counters 
        """
        
        """
        product = counter1 * counter2 * 1.0 
        mag1 = counter1 * counter1 
        mag2 = counter2 * counter2 
        if (mag1 + mag2 - product) == 0.0 :
            similarity = 0.0 
        else:
            similarity = product / (mag1 + mag2 - product)
        return similarity 
        """
        
        mag1 = len(counter1)
        mag2 = len(counter2)
        product = 0.0 
        for item in counter1:
            if item in counter2:
                product += 1.0
        if (mag1 + mag2 - product) == 0:
            similarity = 0.0
        else:
            similarity = product / float(mag1 + mag2 - product)
        return similarity  

    def getRoomIdBySsid(self, ssid):
        wifiCounter = self.parseWifiRaw2Counter(ssid)
        if len(wifiCounter) == 0:
            return 0
        
        # No room record yet, just add new room 
        if len(self.rooms) == 0:
            newRoomId = self.mysqlHelper.insertNewRoom(self.cid, ssid) 
            if newRoomId > 0:
                newRoom = RoomData(newRoomId, ssid)
                self.rooms.append(newRoom)
                return newRoomId
            else:
                return 0 
        
        similarityList = list() 
        roomList = list()
        for room in self.rooms:
            roomList.append(room.roomId) 
            roomSignature = room.wifiDict
            #similarityList.append(self.getCosineSimilarity(wifiCounter, roomSignature)) 
            similarityList.append(self.getTanimotoSimilarity(wifiCounter, roomSignature))
        maxSimilarityIdx, maxSimilarityVal = max(enumerate(similarityList), key = operator.itemgetter(1))
        # Find the best matched room 
        if maxSimilarityVal >= ROOM_SIMILARITY_THRESHOLD:
            return roomList[maxSimilarityIdx] 
        else:
            newRoomId = self.mysqlHelper.insertNewRoom(self.cid, ssid)
            if newRoomId > 0:
                newRoom = RoomData(newRoomId, ssid)
                self.rooms.append(newRoom) 
                return newRoomId
            else:
                return 0 
        

    