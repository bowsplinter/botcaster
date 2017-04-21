from django.db import models

from accounts.models import User

# Create your models here.
class Link(models.Model):
    author = models.ForeignKey(User, related_name = 'link')
    link = models.CharField(max_length = 140)
    description = models.CharField(max_length = 200)

    def __str__(self):
        return self.link

class Like(models.Model):
    link = models.ForeignKey(Link, related_name = 'liked_link')
    user = models.ForeignKey(User, related_name = 'liked_by')

    def __str__(self):
        return '{} : {}'.format(
            self.user, 
            self.post
        )