from django.db import models
from django.forms import model_to_dict
from tsubuyaki.models.account import Account
from tsubuyaki.models.post import Post

# favorite エンティティ
class Favorite(models.Model):

    favorite_id = models.IntegerField(primary_key = True)
    post = models.ForeignKey(Post,on_delete = models.CASCADE)
    account = models.ForeignKey(Account,on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = "favorite"

    def to_dict(self):
        return model_to_dict(self)