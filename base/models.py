from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User


def EET_time():
    return datetime.now() + timedelta(hours=2)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(default=EET_time)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete', '-create']
