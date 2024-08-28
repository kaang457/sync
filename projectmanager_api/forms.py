from django import forms
from projectmanager.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["description", "dueDate", "startDate", "assignee"]
