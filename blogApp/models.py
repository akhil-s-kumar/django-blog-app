from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from ckeditor.fields import RichTextField

# Create your models here.
class Categories(models.Model):
    categoryname = models.CharField(max_length=255)

    def __str__(self):
        return self.categoryname

class Post(models.Model):
    title = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=255, default='Blog Post')
    slug = models.SlugField(max_length=255, null=True, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='blog', null=True)
    body = RichTextField(blank=False, null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categories, null=True, on_delete=models.PROTECT, related_name='category_set')

    def __str__(self):
        return self.title + ' | ' + str(self.author)
