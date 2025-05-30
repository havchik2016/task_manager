from django.db import models
import datetime


# Create your models here.

class Task(models.Model):
    PROJECT_TYPES = [("Private", "Private"), ("Public", "Public")]
    STATUSES = [("In Queue", "In Queue"), ("In Progress", "In Progress"),
                ("Complete", "Complete")]
    PRIORITIES = [("Low", "Low"), ("Medium", "Medium"), ("High", "High")]
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.CharField(max_length=100, default="project1")
    deadline = models.DateTimeField(default=datetime.date(2026, 1, 31))
    user = models.CharField(max_length=100, default="user1")
    status = models.CharField(max_length=12, choices=STATUSES, default="In Queue")
    priority = models.CharField(max_length=7, choices=PRIORITIES, default="Low")

    def __str__(self):
        return self.name


class User(models.Model):
    user = models.CharField(max_length=100, default="user1")

    @classmethod
    def create(cls, name):
        user_obj = cls(user=name)
        return user_obj

    def __str__(self):
        return self.user


class Filter(models.Model):
    PRIORITIES = [("None", "None"), ("Low", "Low"),
                  ("Medium", "Medium"), ("High", "High")]
    STATUSES = [("None", "None"), ("In Queue", "In Queue"),
                ("In Progress", "In Progress"), ("Complete", "Complete")]
    priority_filter = models.CharField(max_length=100, choices=PRIORITIES, default="None")
    status_filter = models.CharField(max_length=100, choices=STATUSES, default="None")


class Project(models.Model):
    PROJECT_TYPES = [("Private", "Private"), ("Public", "Public")]
    project_name = models.CharField(max_length=100, default='project1')
    project_type = models.CharField(max_length=10, choices=PROJECT_TYPES, default='Public')
    project_description = models.TextField(default='')