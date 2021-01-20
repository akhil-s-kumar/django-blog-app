from django.urls import path
from . import views
from .views import blog


urlpatterns = [
path('', blog.as_view(), name="blog"),
]
