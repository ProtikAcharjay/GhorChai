from django_q.tasks import async_task
from django.contrib.auth.models import User
from .models import Notification, Post

def send_post_notifications(post_id, username):
    post = Post.objects.get(id=post_id)
    users = User.objects.exclude(id=post.owner.id)
    
    for user in users:
        Notification.objects.create(
            user=user,
            post=post,
            message=f"{username} posted: {post.title}"
        )

def schedule_notifications(post_id, username):
    async_task(send_post_notifications, post_id, username)
