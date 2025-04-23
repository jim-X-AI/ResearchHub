from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Topic(models.Model):
    """Where users can store what they learnt and records the time"""
    text = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Returns a string representation of the model"""
        return self.text


class Entry(models.Model):
    """Many-to-one relationship, where users can enter what they learn"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    # noinspection PyTypeChecker
    def __str__(self):
        """Returns a short text of what the user has learned"""
        return f'{self.text[:50]}' if len(self.text) > 50 else self.text


class LearningEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    entry = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns a string representation of the model"""
        return self.text
