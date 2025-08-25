from django.test import TestCase , SimpleTestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import Task
from .forms import TaskForm


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


class TaskFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'title':'new task',
            'description':'some description',
            'is_completed':False,
            'priority':'M',
            'due_date':(timezone.now() + timedelta(days=1)).date(),
        }
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid(), f"Form should be valid, but got errors: {form.errors}")

    def test_due_date_in_past_invalid(self):
        data = {
            'title':'old task',
            'description':'Invalid past date',
            'is_completed':False,
            'priority':'M',
            'due_date':(timezone.now() - timedelta(days=1)).date(),
        }
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid(), 'Form should not be valid with a past due date')
        self.assertIn('due_date',form.errors, 'Due date error should be raised')
        
    def test_missing_title_invalid(self):
        data = {
            'title':'',
            'description':'Invalid past date',
            'is_completed':False,
            'priority':'M',
            'due_date':(timezone.now() + timedelta(days=2)).date(),
        }
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid(), f'Form should not be valid without a title{form.errors}')
        self.assertIn('title',form.errors , 'Title error should be raised')

