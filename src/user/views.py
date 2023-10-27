from django.shortcuts import render
from django.views.generic.edit import FormView
# from .forms import CustomUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# class CustomUserCreate(FormView):
#     # ログイン前
#     form_class = CustomUserForm  # フォームを指定する



def signup_email(request):
    return render(request, 'user/signup_email.html')
def check_email(request):
    return render(request, 'user/check_email.html')