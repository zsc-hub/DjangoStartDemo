#enconding=utf-8
from django.conf.urls import url
from . import views

app_name='blog'
urlpatterns = [
    url(r'^$', views.blog_title, name='blog_title'),
    # views.blog_article 也可以写成"views.blog_article",两种写法没有什么区别，只要保证在同一个项目中保持一致即可
    url(r'(?P<article_id>\d)/$', views.blog_article, name="blog_detail"),
]