from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
# from .models import Diary, emotion
# from user.models import CustomUser

def account_delete_success(request):
    return render(request, 'diary/account_delete_success.html')

def account_delete(request):
    return render(request, 'diary/account_delete.html')

def base(request):
    return render(request, 'diary/base.html')

def calendar_month(request):
    return render(request, 'diary/calendar_month.html')

def calender_week(request):
    return render(request, 'diary/calender_week.html')

def create_diary_confirmation(request):
    return render(request, 'diary/create_diary_confirmation.html')

def create_diary(request):
    return render(request, 'diary/create_diary.html')

def diary_delete(request):
    return render(request, 'diary/diary_delete.html')

def diary_graph(request):
    return render(request, 'diary/diary_graph.html')

def diary_home(request):
    return render(request, 'diary/diary_home.html')

def diary_update(request):
    return render(request, 'diary/diary_update.html')

def help_calender(request):
    return render(request, 'diary/help_calender.html')

def help_diary_edit(request):
    return render(request, 'diary/help_diary_edit.html')

def help_diary(request):
    return render(request, 'diary/help_diary.html')

def help_graph(request):
    return render(request, 'diary/help_graph.html')

def help(request):
    return render(request, 'diary/help.html')

def home_top(request):
    return render(request, 'diary/home_top.html')

def loading(request):
    return render(request, 'diary/loading.html')

def logout_success(request):
    return render(request, 'diary/logout_success.html')

def logout(request):
    return render(request, 'diary/logout.html')


def member_information_edit_cancel(request):
    return render(request, 'diary/member_information_edit_cancel.html')

def member_information_edit_check(request):
    return render(request, 'diary/logout.html')

def member_information_edit_comp(request):
    return render(request, 'diary/member_information_edit_comp.html')

def member_information_edit(request):
    return render(request, 'diary/member_information_edit.html')

def member_information(request):
    return render(request, 'diary/member_information.html')

def month_graph(request):
    return render(request, 'diary/month_graph.html')

def positive_conversion(request):
    return render(request, 'diary/positive_conversion.html')

def setting(request):
    return render(request, 'diary/setting.html')

def today_counseling(request):
    return render(request, 'diary/today_counseling.html')

def today_diary_detail(request):
    return render(request, 'diary/today_diary_detail.html')

def week_graph(request):
    return render(request, 'diary/week_graph.html')