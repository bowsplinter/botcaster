from django.db import models

# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key = True)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    username = models.CharField(max_length = 30)

    state = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        self.save()

class Connection(models.Model):
    follower = models.ForeignKey(User, related_name='follower')
    following = models.ForeignKey(User, related_name='following')

    def __str__(self):
        return "{} : {}".format(
            self.follower.username,
            self.following.username
        )