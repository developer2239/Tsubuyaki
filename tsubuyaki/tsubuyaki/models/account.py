from django.db import models
from django.db.models import Q 
from django.http import HttpResponse
from django.shortcuts import render

from django.utils import timezone

# account エンティティ
class Account(models.Model):

    account_id = models.IntegerField(primary_key = True)
    id = models.CharField(primary_key = True, max_length = 10)
    name = models.CharField(max_length = 10)
    password = models.CharField(max_length = 256)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "account"
