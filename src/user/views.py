from django.shortcuts import render
from .models import CustomUser
from .forms import CustomUserForm
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

class PersonCreateView(CreateView):
    model = CustomUser#モデルを指定する
    form_class = CustomUserForm#フォームを指定する
    template_name = "user/singup.html"#テンプレートを指定する
    success_url = reverse_lazy("list") #フォーム送信完了後の遷移ページを指定する
    
def signup(request):
    return render(request, 'user/signup.html')
def signup_email(request):
    return render(request, 'user/signup_email.html')
def check_email(request):
    return render(request, 'user/check_email.html')