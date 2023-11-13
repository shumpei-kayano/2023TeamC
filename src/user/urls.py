from django.urls import path
from user import views

app_name = 'user'
urlpatterns = [
    path('account_top/', views.account_top,name='account_top'),
    path('tutorial1/', views.tutorial1,name='tutorial1'),
    ]    