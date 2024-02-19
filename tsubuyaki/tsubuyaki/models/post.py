import json
from django.db import models
from django.forms import model_to_dict
from tsubuyaki.models.account import Account
import json
from django.db import models as django_models
from django.db.models.query import QuerySet

# post エンティティ
class Post(models.Model):

    post_id = models.IntegerField(primary_key = True)
    account = models.ForeignKey(Account,on_delete = models.CASCADE)
    content = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    favorites = models.ManyToManyField("favorite")

    class Meta:
        db_table = "post"
    
    def to_dict(self):    
        return {
            'post_id': self.post_id,
            'post_content' : self.content,
            'created_at' : self.created_at.strftime("%y年%m月%d日 %H:%M"),
            'name': self.account.name,
            'id': self.account.id,
            'account_id': self.account.account_id,
            'favorite_count' : self.favorites.count(),
        }

class ExtendedJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, django_models.Model) and hasattr(obj, 'to_dict'):
            return obj.to_dict()
        if isinstance(obj, QuerySet):
            return list(obj)
        json.JSONEncoder.default(self, obj)
