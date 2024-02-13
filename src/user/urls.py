from django.urls import path
from user import views
from django.urls import path, include
from .views import CustomSignupView
from django.contrib.auth.views import LoginView


app_name = 'user'
urlpatterns = [
    path('account_top/', views.account_top,name='account_top'),
    path('tutorial1/', views.tutorial1,name='tutorial1'),
    path('logout', views.logout,name='logout'),
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    path('password_reset', views.password_reset,name='password_reset'),
    path('email', views.email,name='email'),
    ]