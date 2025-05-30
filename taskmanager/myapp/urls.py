from django.urls import path
from . import views

# Define a list of url patterns

urlpatterns = [
    path('', views.task_list_view, name='task_list'),
    path('edit/<int:pk>/', views.task_edit_view, name='task_edit'),
    path('delete/<int:pk>/', views.task_delete_view, name='task_delete'),
    path('pedit/<int:pk>/', views.project_edit_view, name='project_edit'),
    path('adduser/<int:pk>/', views.add_user_view, name='add_user')
]