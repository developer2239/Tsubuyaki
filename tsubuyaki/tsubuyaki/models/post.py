from django.db import models

# post エンティティ
class Post(models.Model):

    post_id = models.IntegerField(primary_key = True)
    account_id = models.IntegerField()
    content = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "post"
