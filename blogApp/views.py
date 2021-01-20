from django.shortcuts import render
from django.views.generic import ListView
from .models import Post, Categories
from django.core.paginator import Paginator

# Create your views here.
class blog(ListView):
   model = Post
   template_name = 'index.html'
   context_object_name = 'posts'
   cats = Categories.objects.all()
   ordering = ['-post_date']  
   paginate_by = 2

   def get_context_data(self, *args, **kwargs):
      cat_list = Categories.objects.all()
      latestpost_list = Post.objects.all().order_by('-post_date')[:3]
      context = super(blog, self).get_context_data(*args, **kwargs)
      context["cat_list"] = cat_list
      context["latestpost_list"] = latestpost_list
      return context
