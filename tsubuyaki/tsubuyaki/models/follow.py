from django.db import models
from tsubuyaki.models.account import Account

# follow エンティティ
class Follow(models.Model):

    account_id = models.IntegerField(primary_key = True)
    follow_account = models.ForeignKey(Account,on_delete = models.CASCADE)

    class Meta:
        db_table = "follow"