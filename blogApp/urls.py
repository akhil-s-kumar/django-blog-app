from django.urls import path
from . import views
from .views import blog, search


urlpatterns = [
path('', blog.as_view(), name="blog"),
path('search', search, name="search"),
]
