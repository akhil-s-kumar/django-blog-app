from django.urls import path
from . import views
from .views import blog, search, CategoryView


urlpatterns = [
path('', blog.as_view(), name="blog"),
path('search', search, name="search"),
path('category/<str:cats>/', CategoryView, name="category"),
]
