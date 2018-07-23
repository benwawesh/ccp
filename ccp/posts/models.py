from django.db import models
from django.contrib.auth.models import User
from accounts.models import WebUser

# Create your models here.

class Post(models.Model):
    content = models.CharField(max_length=1000, null=False, blank=False)
    up_vote = models.IntegerField(null=True, blank=True)
    up_vote_count = models.IntegerField(default=0)
    down_vote = models.IntegerField(null=True, blank=True)
    down_vote_count = models.IntegerField(default=0)
    post_votes = models.CharField(max_length=20, null=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField()


    class Meta:
        db_table = 'Post'


class Voter(models.Model):
    post = models.ForeignKey(Post, null=False, blank=False, on_delete=models.CASCADE)
    post_voter = models.ForeignKey(WebUser, null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post", "post_voter")