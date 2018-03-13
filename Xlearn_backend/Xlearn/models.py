
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import datetime
import time



class Network(models.Model):
    name = models.CharField(max_length=256, null=True, default=None)
    parameters = models.CharField(max_length=512, null=True, default=None)
    type = models.CharField(max_length=256, null=True, default=None)


class Optimizer(models.Model):
    name = models.CharField(max_length=256, null=True, default=None)
    parameters = models.CharField(max_length=512, null=True, default=None)
    models.CharField(max_length=256, null=True, default=None)


class Loss(models.Model):
    name = models.CharField(max_length=256, null=True, default=None)
    parameters = models.CharField(max_length=512, null=True, default=None)
    models.CharField(max_length=256, null=True, default=None)


class Manager(models.Model):
    companyName = models.CharField(max_length=256, default="Anonymous")
    email = models.EmailField()
    logo_url = models.CharField(max_length=256, null=True, default=None)
    autoReplyName = models.CharField(max_length=64, blank=True)
    autoReplyImage_url = models.CharField(max_length=256)
    isVIP = models.BooleanField(default=False)
    joinUpNum = models.IntegerField(default=1)
    hangUpTime = models.IntegerField(default=3)  # 分钟
    confirmTime = models.IntegerField(default=3)  # 分钟
    ALLOT_CHOICES = (
        (1, 'turn'),
        (2, 'average'),
        (3, 'return'),
    )
    allotMethod = models.IntegerField(choices=ALLOT_CHOICES, default=1)
    workStart = models.TimeField(default=datetime.time(hour=8))
    workEnd = models.TimeField(default=datetime.time(hour=17))
    verification = models.CharField(max_length=10, null=True, default=None)
    verificationTime = models.DateTimeField(null=True, default=None)


class Task(models.Model):
    config = models.CharField(max_length=1024, null=True, default=None)
    creator = models.ForeignKey(User, related_name="creator_name")
    name = models.CharField(max_length=256, null=True, default=None)
    description = models.CharField(max_length=256, null=True, default=None)
    instance = models.ForeignKey('Instance', related_name="instance_name")
    created_at = models.DateTimeField(null=True, default=None)
    ALLOT_CHOICES = (
        (1, 'deployed'),
        (2, 'running'),
        (3, 'finished'),
        (4, 'canceled'),
    )

    ALLOT_CHOICES_MODEL = (
        (1, 'photo'),
        (2, 'video'),
    )

    ALLOT_CHOICES_TYPE = (
        (1, 'classification'),
        (2, 'detection'),
        (3, 'hashing'),
    )
    status = models.IntegerField(choices=ALLOT_CHOICES, default=1)
    input_model = models.IntegerField(choices=ALLOT_CHOICES_MODEL, default=1)
    type = models.IntegerField(choices=ALLOT_CHOICES_TYPE, default=1)

    dataset = models.ForeignKey('Dataset', related_name="task_dataset")


class Dataset(models.Model):
    link = models.CharField(max_length=256, null=True, default=None)
    path = models.CharField(max_length=256, null=True, default=None)
    ALLOT_CHOICES = (
        (1, 'deployed'),
        (2, 'downloaded'),
        (3, 'deleted'),
    )

    status = models.IntegerField(choices=ALLOT_CHOICES, default=1)
    task = models.ForeignKey(Task, related_name="task_name")
    instance = models.ForeignKey('Instance', related_name="instance_name")


class UserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="extension")
    isManager = models.BooleanField(default=False)
    manager = models.OneToOneField(Manager, on_delete=models.CASCADE, related_name="extension", null=True)


class Instance(models.Model):
    config = models.CharField(max_length=256, null=True, default=None)
    creator = models.ForeignKey(User, related_name="creator_name")
    task = models.ForeignKey(Task, related_name="task_name")
    created_at = models.DateTimeField(null=True, default=None)
    ALLOT_CHOICE_STATUS = (
        (1, 'normal'),
        (2, 'deleted'),
    )
    ALLOT_CHOICE_MODEL = (
        (1, 'photo'),
        (2, 'video'),
    )
    ALLOT_CHOICES_TYPE = (
        (1, 'classification'),
        (2, 'detection'),
        (3, 'hashing'),
    )
    status = models.IntegerField(choices=ALLOT_CHOICE_STATUS, default=1)
    input_model = models.IntegerField(choices=ALLOT_CHOICE_MODEL, default=1)
    type = models.IntegerField(choices=ALLOT_CHOICES_TYPE, default=1)
    run_time = models.IntegerField(default=0)
    dataset = models.ForeignKey(Dataset, related_name="instance_dataset")


















