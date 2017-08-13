# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class ChatMessage(models.Model):
    room = models.CharField(max_length=20)
    message = models.CharField(max_length=100)
    name = models.CharField(max_length=20)
