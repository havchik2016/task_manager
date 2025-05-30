from django import forms
from .models import Task, User, Filter, Project

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline',
                  'status', 'priority', 'project']


class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ['priority_filter', 'status_filter']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_description', 'project_type']