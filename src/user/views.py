from django.shortcuts import render
from django.views.generic.edit import FormView
# from .forms import CustomUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

def account_top(request):
    return render(request, 'account_top.html')

def tutorial1(request):
    return render(request, 'tutorial1.html')

def logout(request):
    return render(request, 'logout.html')