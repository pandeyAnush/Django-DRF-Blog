
from django.urls import path
# For example, in another app's views.py
from .views import BlogView, PublicBlogView

urlpatterns = [
    path('blog/', BlogView.as_view()),
    path('public/blogs/', PublicBlogView.as_view(), name='public-blogs'),
]




