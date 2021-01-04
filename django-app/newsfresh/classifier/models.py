from django.db import models


# Create your models here.
class NewsInfo(models.Model):
    user_input = models.TextField(default=" ")
    news_link = models.TextField(default=" ")
    news_title = models.TextField(default=" ")
    news_text = models.TextField(default=" ")
    output = models.TextField(default=" ")
    objects = models.Manager()
