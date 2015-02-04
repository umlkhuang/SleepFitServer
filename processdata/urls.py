from django.conf.urls import patterns, url

from processdata import views , processUpload

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    url(r'^upload$', views.upload_file, name = 'upload'),
    url(r'^uploadSurvey$', views.upload_survey, name = 'upload survey'), 
    url(r'^getMobilityByHour$', views.get_user_mobility_by_hour, name = "mobility by hour"),
    url(r'^getMobilityByDay$', views.get_user_mobility_by_day, name = "mobility by day"),
    url(r'^getUsageByHour$', views.get_user_app_usage_by_hour, name = "app usage by hour"),
    url(r'^getUsageByDay$', views.get_user_app_usage_by_day, name = "app usage by hour"),
    url(r'^getLifestyle$', views.get_user_lifestyle, name = "lifestyle by day"),
    url(r'^getSleep$', views.get_sleep_info, name = "get sleep info"),
    url(r'^jingUpload$', views.upload_Jing_file, name = "upload file for Jing")
)