from django.urls import path
from django.views.generic import TemplateView

app_name = 'projectmanager'

urlpatterns = [
    path('', TemplateView.as_view(template_name="projectmanager/index.html"))
]