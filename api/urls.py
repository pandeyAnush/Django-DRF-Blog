from django.contrib import admin
from django.urls import path,include
from home.views import PublicBlogView

urlpatterns = [
    path('account/', include('account.urls')),
    path('home/', include('home.urls')),
    path('public/blogs/', PublicBlogView.as_view(), name='public-blogs'),

    
]
