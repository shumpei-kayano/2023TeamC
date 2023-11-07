from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .models import Diary, Emotion
from user.models import CustomUser
from django.contrib.auth.decorators import login_required
from .forms import DiaryCreateForm


@login_required
def account_delete_success(request):
    return render(request, 'diary/account_delete_success.html')
  
@login_required
def account_delete(request):
    return render(request, 'diary/account_delete.html')

@login_required
def base(request):
    return render(request, 'diary/base.html')

@login_required
def calendar_month(request):
    return render(request, 'diary/calendar_month.html')

@login_required
def calender_week(request):
    return render(request, 'diary/calender_week.html')

@login_required
def create_diary_confirmation(request):
  if request.method == 'POST':
    # 保存ボタンがクリックされた場合
    form = DiaryCreateForm(request.POST, request.FILES)
    if form.is_valid():
        new_diary = form.save(commit=False)
        new_diary.user = request.user  # ログイン中のユーザーを設定
        new_diary.save()  # データベースに保存
        return render(request, 'diary/create_diary_confirmation.html', {'form': form})
  else:
      form = DiaryCreateForm()
      return render(request, 'diary/create_diary.html', {'Diary': form})

@login_required
def create_diary(request):
    form = DiaryCreateForm()
    return render(request, 'diary/create_diary.html',{'Diary':form})

@login_required
def diary_delete(request):
    return render(request, 'diary/diary_delete.html')

@login_required
def diary_graph(request):
    return render(request, 'diary/diary_graph.html')

@login_required
def diary_home(request):
    return render(request, 'diary/diary_home.html')

@login_required
def diary_update(request):
    return render(request, 'diary/diary_update.html')

@login_required
def help_calender(request):
    return render(request, 'diary/help_calender.html')

@login_required
def help_diary_edit(request):
    return render(request, 'diary/help_diary_edit.html')

@login_required
def help_diary(request):
    return render(request, 'diary/help_diary.html')

@login_required
def help_graph(request):
    return render(request, 'diary/help_graph.html')

@login_required
def help(request):
    return render(request, 'diary/help.html')

@login_required
def home_top(request):
    return render(request, 'diary/home_top.html')

@login_required
def loading(request):
    return render(request, 'diary/loading.html')

@login_required
def logout_success(request):
    return render(request, 'diary/logout_success.html')

@login_required
def logout(request):
    return render(request, 'diary/logout.html')

@login_required
def member_information_edit_cancel(request):
    return render(request, 'diary/member_information_edit_cancel.html')

@login_required
def member_information_edit_check(request):
    return render(request, 'diary/logout.html')

@login_required
def member_information_edit_comp(request):
    return render(request, 'diary/member_information_edit_comp.html')

@login_required
def member_information_edit(request):
    return render(request, 'diary/member_information_edit.html')

@login_required
def member_information(request):
    return render(request, 'diary/member_information.html')

@login_required
def month_graph(request):
    return render(request, 'diary/month_graph.html')

@login_required
def positive_conversion(request):
    return render(request, 'diary/positive_conversion.html')

@login_required
def setting(request):
    return render(request, 'diary/setting.html')

@login_required
def today_counseling(request):
    return render(request, 'diary/today_counseling.html')

@login_required
def today_diary_detail(request):
    if request.method == 'POST':
      return render(request, 'diary/today_diary_detail.html')
    else:
      form = DiaryCreateForm()
      return render(request, 'diary/create_diary.html',{'Diary':form})
    
@login_required
def week_graph(request):
    return render(request, 'diary/week_graph.html')

