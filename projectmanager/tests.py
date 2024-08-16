# coverage run --omit='*/venv/*' manage.py test
from django.test import TestCase
from django.contrib.auth.models import User
from .models import *


class Test_Create_TaskLog(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_client = Client.objects.create(name="X")
        test_project = Project.objects.create(name="P1", client=test_client)
        test_task = Issue.objects.create(
            project=test_project,
            description="Test Task",
            slug="TEST",
            due_date=None,
        )
        testuser1 = User.objects.create_user(
            username="test_user1", password="123456789"
        )
        test_tasklog = Log.tasklogobjects.create(task=test_task)

    def test_log_content(self):
        tasklog = Log.tasklogobjects.get(id=1)
        status = f"{tasklog.status}"
        is_billable = f"{tasklog.is_billable}"
        user = f"{tasklog.user}"
        self.assertEqual(user, "test_user1")
        self.assertEqual(status, "waiting")
        self.assertEqual(is_billable, "non-billable")
        self.assertEqual
