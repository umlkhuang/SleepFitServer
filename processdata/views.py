from django.http import HttpResponse
import processUpload 
import processMobility
import processSleepRequest
import simplejson as json

from django.views.decorators.csrf import csrf_exempt
from processdata import processAppUsage
from processLifestyle import getUserLifestyle 
from constants import RAW_FILE_DIR 

def index(request):
    return HttpResponse("Hello, world. You're at the processdata index.")

@csrf_exempt
def upload_file_old(request):
    newFileName = request.POST.get('newFileName', '')
    UUID = request.POST.get('UUID', '')
    accessCode = request.POST.get('accessCode', '')

    if UUID == '' or newFileName == '' or accessCode == '':
        return HttpResponse(status=400)

    filePath = RAW_FILE_DIR + newFileName
    print filePath 
    destination = open(filePath, 'wb+')
    for chunk in request.FILES['file'].chunks():
        destination.write(chunk)
    destination.close()

    processUpload.processUploadedFile(filePath, accessCode, UUID)

    return HttpResponse()

@csrf_exempt
def upload_file(request):
    UUID = request.POST.get('UUID', '')
    accessCode = request.POST.get('accessCode', '')
    fileName = request.POST.get('fileName')
    
    if UUID == '' or accessCode == '':
        return HttpResponse(status=400)
    
    filePath = RAW_FILE_DIR + fileName
    destination = open(filePath, 'wb+')
    for chunk in request.FILES['file'].chunks():
        destination.write(chunk)
    destination.close()

    """
    Need to run this function in another thread for two reasons:
    1. the app can get http response quickly since the file is already uploaded successfully;
    2. when calculating the sleep/wakeup time, we need to load the prediction model, and it needs
    to be run in another thread, otherwise the main thread will be stuck forever
    """
    import threading
    t = threading.Thread(target=processUpload.processSyncData, args=(filePath, accessCode, UUID))
    t.start()
    
    return HttpResponse()

def get_user_mobility_by_hour(request):
    cid = request.GET["cid"]
    date = request.GET["date"] 
    retJSON = ""
    retJSON = json.dumps(processMobility.getMobilityByHour(date, cid)) 
    return HttpResponse(retJSON, content_type='application/json') 
    
def get_user_mobility_by_day(request):
    cid = request.GET["cid"]
    endDate = request.GET["endDate"]
    days = request.GET["days"]
    retJSON = ""
    retJSON = json.dumps(processMobility.getMobilityByDays(endDate, int(days), cid)) 
    return HttpResponse(retJSON, content_type='application/json')

def get_user_app_usage_by_hour(request):
    cid = request.GET["cid"]
    date = request.GET["date"] 
    retJSON = ""
    retJSON = json.dumps(processAppUsage.getAppUsageByHour(date, cid))
    return HttpResponse(retJSON, content_type='application/json')

def get_user_app_usage_by_day(request):
    cid = request.GET["cid"]
    endDate = request.GET["endDate"]
    days = request.GET["days"]
    retJSON = ""
    retJSON = json.dumps(processAppUsage.getAppUsageByDays(endDate, int(days), cid)) 
    return HttpResponse(retJSON, content_type='application/json')

def get_user_lifestyle(request):
    cid = request.GET["cid"]
    trackDate = request.GET["date"]
    retJSON = ""
    retJSON = json.dumps(getUserLifestyle(cid, trackDate));
    return HttpResponse(retJSON, content_type='application/json')

@csrf_exempt
def upload_survey(request):
    UUID = request.POST.get('UUID', '')
    accessCode = request.POST.get('accessCode', '')
    if UUID == '' or accessCode == '':
        return HttpResponse(status=400)
    age = request.POST.get('age', '18')
    gender = request.POST.get('gender', 'Male') 
    racial = request.POST.get('racial', 'A')
    sleepHours = request.POST.get('sleepHours', '8.0') 
    
    processUpload.processUploadSurvey(UUID, accessCode, age, gender, racial, sleepHours)
    return HttpResponse() 

@csrf_exempt
def get_sleep_info(request):
    accessCode = request.GET['accessCode']
    trackDate  = request.GET['trackDate']
    if accessCode == '' or trackDate == '':
        return HttpResponse(status=400)
    retJSON = processSleepRequest.get_sleep_by_day(accessCode, trackDate)
    return HttpResponse(retJSON, content_type='application/json')
    