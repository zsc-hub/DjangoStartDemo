#enconding=utf-8
from django.conf.urls import url
from . import views
# from django.contrib.auth.views import LoginView


app_name='account'
urlpatterns = [
    url(r"^login/$", views.user_login, name="user_login"),
    url(r"^register/$", views.register, name="user_register"),
    url(r"^my-information/$", views.myself, name="my_information"),
    url(r"^edit-my-information/$", views.myself_edit, name="edit_my_information"),
]