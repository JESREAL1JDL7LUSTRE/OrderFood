from django.db import models
from backend.AccountAuth.models import User

# Create your models here.
class PostedContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_content = models.ForeignKey(PostedContent, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)

class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_content = models.ForeignKey(PostedContent, on_delete=models.CASCADE, related_name="shares")
    created_at = models.DateTimeField(auto_now_add=True)

class Reaction(models.Model):
    REACTION_TYPES = [
        ("like", "Like"),
        ("love", "Love"),
        ("haha", "Haha"),
        ("wow", "Wow"),
        ("sad", "Sad"),
        ("angry", "Angry"),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_content = models.ForeignKey(PostedContent, on_delete=models.CASCADE, related_name="reactions")
    type = models.CharField(max_length=10, choices=REACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
