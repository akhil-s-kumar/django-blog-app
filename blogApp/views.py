from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from .models import Post, Categories, PostComment
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, Http404

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

def CategoryView(request, cats):
   if Categories.objects.filter(categoryname=cats).exists():
      category_posts = Post.objects.filter(category__categoryname=cats).order_by('-post_date')
      cat_list = Categories.objects.all()
      latestpost_list = Post.objects.all().order_by('-post_date')[:3]
      paginator = Paginator(category_posts, 2)
      page = request.GET.get('page')
      category_posts = paginator.get_page(page)
      return render(request, 'category_list.html', {'cats':cats, 'category_posts':category_posts, 'cat_list': cat_list, 'latestpost_list':latestpost_list})
   else:
      raise Http404

class blogdetail(DetailView):
   model = Post
   template_name = 'blog_detail.html'

   def get_context_data(self, *args, **kwargs):
      cat_list = Categories.objects.all()
      latestpost_list = Post.objects.all().order_by('-post_date')[:3]
      context = super(blogdetail, self).get_context_data(*args, **kwargs)
      context["cat_list"] = cat_list
      context["latestpost_list"] = latestpost_list
      return context

@login_required(login_url='/login')
def send_comment(request, slug):
   message = request.POST.get('message')
   post_id = request.POST.get('post_id')
   post_comment = PostComment.objects.create(sender=request.user, message=message)
   post = Post.objects.filter(id=post_id).first()
   post.comments.add(post_comment)
   return redirect('.')