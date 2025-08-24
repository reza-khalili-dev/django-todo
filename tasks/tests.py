from django.test import TestCase , SimpleTestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import Task


# Create your tests here.


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='username' , password='password123'
        )
        self.task = Task.objects.create(
            user = self.user,
            title = 'test title',
            description = 'test description',
            is_completed = False,
            priority = 'mediom',
            due_date = timezone.now().date() + timedelta(days=1),
         
        )
        
    def test_task_creation(self):
        self.assertEqual(self.task.title,'test title'),
        self.assertFalse(self.task.is_completed),
        self.assertEqual(self.task.user.username,'username')

    def test_task_str_method(self):
        self.assertEqual(str(self.task),'test title')
    
    def test_due_date_not_in_past(self):
        self.assertGreater(self.task.due_date , timezone.now().date())
    
    