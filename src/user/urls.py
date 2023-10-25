from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('signup_email', views.signup_email,name='signup_email'),
    path('check_email', views.check_email,name='check_email')
]