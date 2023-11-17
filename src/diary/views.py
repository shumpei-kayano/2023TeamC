from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .models import Diary, Emotion
from user.models import CustomUser
from django.contrib.auth.decorators import login_required
from .forms import DiaryCreateForm
from django.shortcuts import get_object_or_404
from datetime import datetime, date
import boto3

# comrehendを使って感情分析を行う関数
def analyze_sentiment(text, diary):
    # 感情分析の生成
    comprehend = boto3.client('comprehend', 'us-east-1')
    result = comprehend.detect_sentiment(Text=text, LanguageCode='ja')

    # 特定のDiaryとユーザーに関連するEmotionオブジェクトが存在するか確認
    existing_emotion = Emotion.objects.filter(diary=diary, diary__user=diary.user).first()

    # Emotion モデルにデータをセット
    if existing_emotion:
        # 特定のDiaryとユーザーに関連するEmotionオブジェクトが存在する場合は上書き保存
        existing_emotion.reasoning = result['Sentiment']
        existing_emotion.positive = result['SentimentScore']['Positive']
        existing_emotion.negative = result['SentimentScore']['Negative']
        existing_emotion.neutral = result['SentimentScore']['Neutral']
        existing_emotion.mixed = result['SentimentScore']['Mixed']
        existing_emotion.save()
    # Emotionオブジェクトが存在しない場合は新しいEmotionオブジェクトを作成して保存
    else:
        new_emotion = Emotion(
            diary=diary,
            reasoning=result['Sentiment'],
            positive=result['SentimentScore']['Positive'],
            negative=result['SentimentScore']['Negative'],
            neutral=result['SentimentScore']['Neutral'],
            mixed=result['SentimentScore']['Mixed'],
            week_number=diary.created_date.isocalendar()[1],
            month=diary.created_date.month,
            day=diary.created_date.day,
            year=diary.created_date.year
        )
        new_emotion.save()



def account_delete_success(request):
    # ログイン中のユーザーアカウントを取得
    user = request.user
    # ユーザに関連するデータを削除
    user_diaries = Diary.objects.filter(user=user)

    # 日記に関連する感情分析データを削除
    for diary in user_diaries:
        Emotion.objects.filter(diary=diary).delete()

    # 日記を削除
    user_diaries.delete()

    # ユーザを削除
    user.delete()
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

def create_diary_confirmation(request):

    if request.method == 'POST':
        form = DiaryCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_diary = form.save(commit=False)
            new_diary.user = request.user
            new_diary.save()  # データベースに保存
            
            # 一旦カレンダーが出来るまで----------------------------------------------------------
            saved_diary = Diary.objects.filter(user=request.user).order_by('-created_date').first()
            #-------------------------------------------------------------------------------------
            
            return redirect('diary:create_diary_confirmation', pk=saved_diary.id)
    else:
        form = DiaryCreateForm()
    return render(request, 'diary/create_diary.html', {'Diary': form})

def create_diary_confirmation2(request, pk):
    # pkからdiaryを取得する
    diary = get_object_or_404(Diary, id=pk)
    # 編集した時の処理
    if request.method == 'POST':
        form = DiaryCreateForm(request.POST, request.FILES, instance=diary)
        if form.is_valid():
            form.save()
            return redirect('diary:create_diary_confirmation', pk=pk)

    # 感情分析の実行関数
    analyze_sentiment(diary.content, diary)
    
    saved_diary = Diary.objects.get(pk=pk)
    return render(request, 'diary/create_diary_confirmation.html', {'saved_diary': saved_diary})


@login_required
def create_diary(request):
    today = date.today()
    # 一旦カレンダーが出来るまで----------------------------------------------------------
    diary = Diary.objects.filter(user=request.user,created_date=today,)
    #-------------------------------------------------------------------------------------
    if diary:
      return render(request, 'diary/today_diary_detail.html', {'diary': diary})

    form = DiaryCreateForm()
    return render(request, 'diary/create_diary.html', {'Diary': form, 'today': today})


@login_required
def diary_delete(request, pk):
    diary = get_object_or_404(Diary, id=pk)
    return render(request, 'diary/diary_delete.html',{'diary': diary})

@login_required
def diary_graph(request):
    return render(request, 'diary/diary_graph.html')

@login_required
def diary_home(request,pk):
    return render(request, 'diary/diary_home.html')


@login_required
def diary_update(request, pk):
    diary = get_object_or_404(Diary, id=pk)
    return render(request, 'diary/diary_update.html',{'diary': diary})

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
    today = date.today()
    diary_today = Diary.objects.filter(user=request.user, created_date=today)
    if diary_today:
        return redirect('diary:today_diary_detail')
    return render(request, 'diary/home_top.html')
    
@login_required
def home_top2(request,pk):
        diary = get_object_or_404(Diary, id=pk)
        emotion = Emotion.objects.get(diary=diary)
        emotion.delete()
        diary.delete()
        return redirect('diary:home_top1')


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
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        request.session['username'] =username
        request.session['email'] =email
    return render(request, 'diary/member_information_edit_check.html', {'username': username, 'email':email})

@login_required
def member_information_edit_comp(request):
    # セッション受け取る
    new_username = request.session.get('username')
    new_email = request.session.get('email')

    # ユーザー情報を取得
    user = request.user

    # ユーザー情報を更新
    if new_username:
        user.username = new_username

    # メールアドレスを更新
    if new_email:
        user.email = new_email

    # セーブ
    user.save()

    # セッションを削除
    request.session.pop('username', None)
    request.session.pop('email', None)

    return render(request, 'diary/member_information_edit_comp.html', {'user': user})

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
    today = date.today()
    diary = get_object_or_404(Diary, user=request.user, created_date=today)
    if diary:
        return render(request, 'diary/today_diary_detail.html', {'diary': diary})
    form = DiaryCreateForm()
    return render(request, 'diary/create_diary.html', {'Diary': form})


@login_required
def today_diary_detail2(request,pk):
    today = date.today()
    diary = get_object_or_404(Diary, user=request.user, created_date=today)
    if diary:
        return render(request, 'diary/today_diary_detail.html', {'diary': diary})
    form = DiaryCreateForm()
    return render(request, 'diary/create_diary.html', {'Diary': form})

@login_required
def week_graph(request):
    return render(request, 'diary/week_graph.html')

@login_required
def today_diary_graph(request):
  return render(request,'diary/today_diary_graph.html')

@login_required
def today_counseling_graph(request):
  return render(request,'diary/today_counseling_graph.html')

@login_required
def record_diary_detail(request):
  return render(request,'diary/record_diary_detail.html')

@login_required
def record_diary_graph(request):
  return render(request,'diary/record_diary_graph.html')

