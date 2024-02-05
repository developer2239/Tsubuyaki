from django.db import models
from tsubuyaki.models.account import Account

# post エンティティ
class Post(models.Model):

    post_id = models.IntegerField(primary_key = True)
    account = models.ForeignKey(Account,on_delete = models.CASCADE)
    content = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "post"
