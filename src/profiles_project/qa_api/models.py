
from django.db import models
from django.contrib.auth.models import AbstractUser
from profiles_api.models import UserProfiles, Superuser, Group


class QAApplication(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    superuser = models.ForeignKey(Superuser, on_delete=models.CASCADE)

class Question(models.Model):
    text = models.TextField()
    application = models.ForeignKey(QAApplication, on_delete=models.CASCADE)

class Answer(models.Model):
    text = models.TextField()
    user = models.ForeignKey(UserProfiles, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.OneToOneField('Score', on_delete=models.CASCADE, null=True, blank=True)

class Score(models.Model):
    value = models.IntegerField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

class DLModel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
