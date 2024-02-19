from django.db import models
from django.forms import model_to_dict 

# account エンティティ
class Account(models.Model):

    account_id = models.IntegerField(primary_key = True)
    id = models.CharField(max_length = 10)
    name = models.CharField(max_length = 10)
    password = models.CharField(max_length = 256)
    profile = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "account"
    
    def to_dict(self):
        return model_to_dict(self)    
