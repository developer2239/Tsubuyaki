from django.db import models
from tsubuyaki.models.account import Account

# follow エンティティ
class Follow(models.Model):

    account = models.ForeignKey(Account,on_delete = models.CASCADE, primary_key = True)
    follow_account = models.ForeignKey(Account,on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = "follow"