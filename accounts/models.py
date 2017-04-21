from django.db import models

# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key = True)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    username = models.CharField(max_length = 30)

    def __str__(self):
        return self.username

class Connection(models.Model):
    follower = models.ForeignKey(User, related_name='follower')
    following = models.ForeignKey(User, related_name='following')

    def __str__(self):
        return "{} : {}".format(
            self.follower.username,
            self.following.username
        )