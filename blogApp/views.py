from django.shortcuts import render
from django.views.generic import ListView
from .models import Post, Categories
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
class blog(ListView):
   model = Post
   template_name = 'blog_list.html'
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

def search(request):
   template = 'search_list.html'
   query = request.GET.get('q')
   if query:
      posts = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)).order_by('-post_date')
   else:
      posts = Post.objects.all()
   
   cat_list = Categories.objects.all()
   latestpost_list = Post.objects.all().order_by('-post_date')[:3]
   paginator = Paginator(posts, 2)
   page = request.GET.get('page')
   posts = paginator.get_page(page)
   return render(request, template, {'posts':posts, 'cat_list': cat_list, 'latestpost_list':latestpost_list, 'query':query})
