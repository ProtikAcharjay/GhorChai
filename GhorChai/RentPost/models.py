from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    price = models.IntegerField()
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner.username} - {self.title}'

class PostReaction(models.Model):
    UPVOTE = 1
    DOWNVOTE = 0
    NO_REACTION = -1
    REACTION_CHOICES = [
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
        (NO_REACTION, 'NoReaction')
    ]
    
    post = models.ForeignKey(Post, related_name='reactions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.IntegerField(choices=REACTION_CHOICES, default=NO_REACTION)
    
    class Meta:
        unique_together = ('post', 'user')
    
    def __str__(self):
        reaction = dict(self.REACTION_CHOICES).get(self.reaction_type, 'NoReaction')
        return f'{self.user.username} reacted on {self.post.title} with {reaction}'
    

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} commented on {self.post.title}'

