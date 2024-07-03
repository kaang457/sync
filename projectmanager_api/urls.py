from django.urls import path
from django.views.generic import TemplateView
from .views import TaskLogDetail, TaskLogList, TaskList
app_name = 'projectmanager_api'

urlpatterns = [
    path('tasklogs/', TaskLogList.as_view(), name = 'listcreate'),
    path('<int:pk>', TaskLogDetail.as_view(), name='detailcreate'),
    path('tasks/', TaskList.as_view(), name='tasklist')
]   