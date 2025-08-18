from django.urls import path
from . import views


urlpatterns = [
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('',views.HomeView.as_view(),name='home'),
    path('tasks/',views.TaskListView.as_view(),name='task_list'),
    path('tasks/create/', views.TaskCreateView.as_view(),name='task_create'),

    

]
