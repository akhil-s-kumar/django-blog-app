from django.urls import path
from . import views
from .views import blog, search, CategoryView, blogdetail


urlpatterns = [
path('', blog.as_view(), name="blog"),
path('search', search, name="search"),
path('category/<str:cats>/', CategoryView, name="category"),
path('<slug:slug>/', blogdetail.as_view(), name="blog-detail"),
]
