from django.db import models

from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from blog.models import BlogPost


class Comment(models.Model):
    Blog = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body[:20]
