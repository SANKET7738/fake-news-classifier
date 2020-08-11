from django.db import models

# Create your models here.

class NewsInfo(models.Model):
    news_link = models.TextField(blank=False)
    news_title = models.TextField(blank=False)
    news_text = models.TextField(blank=False)
    output = models.TextField(blank=False)
    
    