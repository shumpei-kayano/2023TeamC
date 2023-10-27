from django.shortcuts import render
from .models import Diary, emotion
from user.models import CustomUser

def account_delete_success(request):
    return render(request, 'diary/account_delete_success.html')