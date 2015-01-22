from mysqlHelper import MysqlHelper
from time import strftime 
from datetime import datetime

def getUserLifestyle(cid, trackDate):
    mdb = MysqlHelper()
    lifestyleData = mdb.getLifestyleData(cid, trackDate)
    
    ret = dict()
    retList = list() 
    for instance in lifestyleData:
        oneRecord = dict()
        oneRecord["createTime"] = instance.createTime.strftime('%m/%d/%Y %H:%M:%S')
        oneRecord["type"] = instance.typeName 
        oneRecord["typeId"] = instance.typeId 
        oneRecord["logTime"] = instance.logTime.strftime('%m/%d/%Y %H:%M:%S')
        oneRecord["selection"] = instance.selection 
        oneRecord["note"] = instance.note 
        retList.append(oneRecord) 
    
    ret["lifestylelog"] = retList 
    
    return ret 


