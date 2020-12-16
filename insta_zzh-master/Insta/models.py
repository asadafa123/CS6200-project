
from django.db import models
from imagekit.models import ProcessedImageField
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from haystack import indexes





# Create your models here.
class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to ='static/images/profiles',
        format = 'JPEG',
        options = {'quality':100},
        blank = True,
        null = True
    )
    def get_connections(self):
        connections = UserConnection.objects.filter(creator=self)
        return connections

    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers

    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()



class Post(models.Model):
    author =  models.ForeignKey(
        InstaUser,
        on_delete = models.CASCADE,
        related_name = 'my_posts'
    )
    title = models.TextField(blank = True, null = True)
    article = models.TextField(blank = True, null = True)
    description = models.TextField(blank = True, null = True)
    image = ProcessedImageField(
        upload_to ='static/images/posts',
        format = 'JPEG',
        options = {'quality':100},
        blank = True,
        null = True
    )
    posted_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    
    def indexing(self):
        obj = Post(
            posted_on = self.posted_on,
            title = self.title,
            article = self.article, 
            description = self.description
        )
        obj.save()
        return 
    
    
    def get_absolute_url(self):
        return reverse ("post_detail", args = [str(self.id)])

    def get_like_count(self):
        return self.likes.count()

class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set")
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set")

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username

class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        related_name = 'likes')

    user = models.ForeignKey(
        InstaUser,
        on_delete = models.CASCADE,
        related_name = 'likes'
    )

    class Meta:
        unique_together = ['post', 'user']

    def __str__(self):
        return 'Like: ' + self.user.username + 'likes' + str(self.post)
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',)
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.comment

'''
class Blog(models.Model):
    title = models.CharField(_('Title'), max_length=1000)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    body = models.TextField(_('Body'))
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    is_published = models.BooleanField(_('Is published'), default=False)

    def __str__(self):
        return self.title

'''

