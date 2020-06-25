from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.him

USER = settings.AUTH_USER_MODEL

class Items(models.Model):
    """
    This is the models for items
    """
    #parent = models.ForeignKey("self", null = True, on_delete =models.SET_NULL)
    title = models.CharField(max_length = 200, blank = False, null = True)
    author = models.CharField(max_length = 100, blank =True , null = True)
    details = models.TextField(blank=False , null = False )
    #picture = models.ImageField(blank = True, null = True)
    owner = models.ForeignKey(USER, on_delete = models.CASCADE)
    likes = models.ManyToManyField(USER, related_name = 'Items_owner', blank = True,  through="PostLikes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def absolute_url(self):
        return

    @property
    def info_blog(self):
        if self.author is None:
            return "%s: %s: %s: %s"%(self.picture, self.title, self.created_at, self.owner, self.comment_count, self.likes_count, self.repost_count)
        else:
            return "%s: %s: %s: %s"%(self.picture, self.title, self.created_at, self.author, self.comment_count, self.likes_count, self.repost_count)

    @property
    def owner_info(self):
        return self.owner


class Viewers(models.Model):
    #parent = models.ForeignKey("self", null = True, on_delete =models.SET_NULL)
    reference = models.ForeignKey(Items, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    likes = models.ManyToManyField(USER, related_name = 'Viewers_owner', blank = True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
    @property
    def view_opinion(self):
        return "%s: %s: %s: %s"%(self.owner, self.comment, self.created_at, self.likes)

    @property
    def owner_info(self):
        return self.owner

class PostLikes(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Items, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    @property
    def user_info(self):
        return self.user


class SubViewers(models.Model):
    reference = models.ForeignKey(Viewers, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    likes = models.ManyToManyField(USER, related_name = 'SubViewers_owner', blank = True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
    @property
    def view_opinion(self):
        return "%s: %s: %s: %s"%(self.owner, self.comment, self.created_at, self.likes)

    @property
    def owner_info(self):
        return self.owner