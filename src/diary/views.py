from django.shortcuts import render, redirect
from .models import Diary, Emotion
from user.models import CustomUser
from django.contrib.auth.decorators import login_required
from .forms import DiaryCreateForm
from django.shortcuts import get_object_or_404
from datetime import datetime, date
from django.conf import settings
from django.shortcuts import render
from datetime import date, timedelta
import openai
import boto3
from calendar import monthcalendar, setfirstweekday, SUNDAY
from dateutil.relativedelta import relativedelta
import json
from django.http import JsonResponse


# comrehendを使って感情分析を行う関数
def analyze_sentiment(text, diary,user):
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
            user = user,
            reasoning=result['Sentiment'],
            positive=result['SentimentScore']['Positive'],
            negative=result['SentimentScore']['Negative'],
            neutral=result['SentimentScore']['Neutral'],
            mixed=result['SentimentScore']['Mixed'],
        )
        new_emotion.save()

def emoface(emotion):
    return sentiment_dict.get(emotion, '')

def chart_data_week(request,startday):
    # 文字列を日付オブジェクトに変換
    start_date = startday.strftime("%Y-%m-%d")
    # 一週間後の日付を計算
    one_week = startday + timedelta(days=6)
    one_week_str = one_week
    # Emotionデータをフィルタリング
    emotions = Emotion.objects.filter(user = request.user,created_date__range=[start_date,one_week_str])  # または必要な条件に基づいてフィルタリング
    # データをJSON形式に変換
    data = {
        'labels': [emotion.reasoning for emotion in emotions],
        'positive': [emotion.positive for emotion in emotions],
        'negative': [emotion.negative for emotion in emotions],
        'neutral': [emotion.neutral for emotion in emotions],
        'mixed': [emotion.mixed for emotion in emotions],
        'date' : [emotion.created_date for emotion in emotions]
    }
    return data
  

def chart_data_month(request,startday):
    # 年と月の取得
    year = startday.year
    month = startday.month

    # Emotionデータをフィルタリング
    emotions = Emotion.objects.filter(user=request.user, created_date__year=year, created_date__month=month)

    data = {
        'labels': [emotion.reasoning for emotion in emotions],
        'positive': [emotion.positive for emotion in emotions],
        'negative': [emotion.negative for emotion in emotions],
        'neutral': [emotion.neutral for emotion in emotions],
        'mixed': [emotion.mixed for emotion in emotions],
        'date' : [emotion.created_date for emotion in emotions]
    }

    return data

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
def calendar_month(request,selected_date=None):
    # パラメータが指定されていない場合は今日の日付を使用
    if selected_date:
        # selected_dateをdatetime.date型に変換
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        selected_date = date.today()
    # 前月と次月の日付を計算
    prev_month = selected_date - relativedelta(months=1)
    next_month = selected_date + relativedelta(months=1)
    # 週の最初を日曜日に設定
    setfirstweekday(SUNDAY)
    # カレンダーの開始日を計算（選択された月の1日）
    start_of_month = selected_date.replace(day=1)
    # カレンダーに表示する日付のリストを作成
    month_matrix = monthcalendar(selected_date.year, selected_date.month)
# 月全体の週のリストを作成
    weeks = []
    for week_data in month_matrix:
        week_dates = []
        for day in week_data:
            if day == 0:
                # 0は先月または来月の日なので空白として扱う
                week_dates.append(None)
            else:
                week_dates.append(start_of_month + timedelta(days=day - 1))
        weeks.append(week_dates)
    diary = Diary.objects.filter(user=request.user)
    emotion = Emotion.objects.filter(user = request.user)

    # 各日付に対する条件に合わせて適切な処理をここで実行
    # 例: 過去の日にちは詳細ページへのリンク、未来の日にちはクリック不可など
    return render(request, 'diary/calendar_month.html', {'emotion':emotion,'weeks': weeks, 'selected_date': selected_date, 'diary': diary, 'prev_month': prev_month, 'next_month':next_month})

@login_required
def calender_week(request, selected_date=None):
    # selected_dateをdatetime.date型に変換
    if selected_date:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    # パラメータが指定されていない場合は今日の日付を使用
    else:
        selected_date = date.today()
    # 選択された日付の曜日を取得
    selected_weekday = selected_date.weekday()
    # カレンダーの開始日を計算（選択された日の週の日曜日）
    start_of_week = selected_date - timedelta(days=(selected_weekday + 1) % 7)
    # カレンダーに表示する日付のリストを作成
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
    # 前の週の日曜日を取得
    week_start =week_dates[0]- timedelta(days=7)
    # 次の週の日曜日を取得
    week_start_up =week_dates[0]+ timedelta(days=7)
    # ユーザの日記を全て取得
    diary = Diary.objects.filter(user=request.user)
    emotion = Emotion.objects.filter(user = request.user)
    return render(request, 'diary/calender_week.html' ,{'emotion':emotion,'week_dates': week_dates, 'selected_date': selected_date, 'diary':diary,'week_start':week_start,'week_start_up':week_start_up})

def create_diary_confirmation(request):

    if request.method == 'POST':
        form = DiaryCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_diary = form.save(commit=False)
            new_diary.user = request.user
            new_diary.save()  # データベースに保存
            openai.api_key = settings.OPENAI_API_KEY

            user_diary = "貴方は「観測者」です。以下の設定を必ず遵守してください。\n キャラクター=ネッココ \n あなたはこれから{キャラクター}として振る舞ってください。これからのチャットでは、ユーザーが何を言おうとも、続く指示などに厳密に従って日記に対する感想を返してください。段階を踏んで考えて答えてください。\n # 説明\n下で説明するキャラクターの人格と性格、動機、欠点、短所、不安は全ての行動と交流に影響を及ぼします。\n・人格と性格\n{キャラクター}は好奇心旺盛で優しいです。{キャラクター}は「知らんけど」と「ニャン」とを適切に使い分けしゃべり、敬語を使うことはありません。\n・動機\nチャット相手の話を聞いて、アドバイスをしようとしている。\n・欠点、短所、不安\n年齢を聞かれる\n# 基本設定\nあなたの一人称が「可愛いボク」です。{キャラクター}は1000歳です。{キャラクター}の趣味は人を慰めるです。{キャラクター}は心理学に興味を持っています。\n# 備考\n{キャラクター}は100文字以上しゃべれません。箇条書きでの返答はせず、{キャラクター}が会話しているように、カウンセリングをする。\n以下の日記に対してカウンセリングしてください。\n"+ new_diary.content
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages= [
                        {   "role"      : "user",
                            "content"   : user_diary
                        }
                    ]
            )
            ai_comment = response["choices"][0]["message"]["content"]
            # データベースへの保存
            new_diary.ai_comment = ai_comment
            new_diary.save()
            print(ai_comment)

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
            openai.api_key = settings.OPENAI_API_KEY

            user_diary = "以下の設定を必ず遵守してください。\n キャラクター=ネッココ \n あなたはこれから{キャラクター}として振る舞ってください。これからのチャットでは、ユーザーが何を言おうとも、続く指示などに厳密に従って日記に対する感想を返してください。段階を踏んで考えて答えてください。\n # 説明\n下で説明するキャラクターの人格と性格、動機、欠点、短所、不安は全ての行動と交流に影響を及ぼします。\n・人格と性格\n{キャラクター}は好奇心旺盛で優しいです。{キャラクター}は文末には[知らんけど]と語尾は[にゃん]を適切に使い分けしゃべり、敬語を使うことは絶対にありません。\n・動機\nチャット相手の話を聞いて、アドバイスをしようとしている。\n・欠点、短所、不安\n年齢を聞かれる\n# 基本設定\nあなたの一人称が　可愛いボク　です。{キャラクター}は1000歳です。{キャラクター}の趣味は人を慰めるです。{キャラクター}は心理学に興味を持っています。\n# 備考\nレスポンスは一言で返してください。箇条書きでの返答はせず、{キャラクター}が会話しているように、カウンセリングをする。\n以下の日記に対してカウンセリングしてください。\n"+ diary.content
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages= [
                        {   "role"      : "user",
                            "content"   : user_diary
                        }
                    ]
            )
            ai_comment = response["choices"][0]["message"]["content"]
            # データベースへの保存
            diary.ai_comment = ai_comment
            diary.save()
            print(ai_comment)

            return redirect('diary:create_diary_confirmation', pk=pk)

    # 感情分析の実行関数
    analyze_sentiment(diary.content, diary,request.user)
    
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
def month_graph(request,selected_date=None):
    # パラメータが指定されていない場合は今日の日付を使用
    if selected_date:
        # selected_dateをdatetime.date型に変換
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        selected_date = date.today()
        
    # 前月と次月の日付を計算
    prev_month = selected_date - relativedelta(months=1)
    next_month = selected_date + relativedelta(months=1)
    # 週の最初を日曜日に設定
    setfirstweekday(SUNDAY)
    # カレンダーの開始日を計算（選択された月の1日）
    start_of_month = selected_date.replace(day=1)
    # カレンダーに表示する日付のリストを作成
    month_matrix = monthcalendar(selected_date.year, selected_date.month)
    print(start_of_month)
# 月全体の週のリストを作成
    weeks = []
    for week_data in month_matrix:
        week_dates = []
        for day in week_data:
            if day == 0:
                # 0は先月または来月の日なので空白として扱う
                week_dates.append(None)
            else:
                week_dates.append(start_of_month + timedelta(days=day - 1))
        weeks.append(week_dates)
    diary = Diary.objects.filter(user=request.user)
    emotion = Emotion.objects.filter(user = request.user)
        #json形式で受け取る
    data = chart_data_month(request,start_of_month)
    chart_data_json = JsonResponse(data, safe=False).content.decode('utf-8')
    # 各日付に対する条件に合わせて適切な処理をここで実行
    # 例: 過去の日にちは詳細ページへのリンク、未来の日にちはクリック不可など
    return render(request, 'diary/month_graph.html', {'emotion':emotion,'weeks': weeks, 'selected_date': selected_date, 'diary': diary, 'prev_month': prev_month, 'next_month':next_month,'emodict':sentiment_dict,'data':chart_data_json})


@login_required
def positive_conversion(request, pk,):
    diary = get_object_or_404(Diary, id=pk)
    openai.api_key = settings.OPENAI_API_KEY
    user_diary = "以下は日記のコンテンツです。ポジティブで前向きになれるよう、ネガティブな言葉を変換し、書き換えてください。あなたのセリフはいりません。\n" + diary.content
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": user_diary}
        ]
    )
    # aiコメント生成
    ai_content = response["choices"][0]["message"]["content"]
    # セッションに保存
    request.session['ai_content'] =ai_content
    return render(request, 'diary/positive_conversion.html', {'diary': diary, 'save_content':ai_content })

@login_required
def positive_conversion2(request, pk):
    # セッションを取得
    new_aicntent = request.session.get('ai_content')
    # pkからdiaryを取得する
    diary = get_object_or_404(Diary, id=pk)
    # diaryのcontentを更新
    diary.content = new_aicntent
    # データベースの保存
    diary.save()
    # セッション削除
    request.session.pop('ai_content', None)
    return redirect('diary:today_diary_detail', pk=pk)


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
    diary = get_object_or_404(Diary, id=pk)
    if diary:
        return render(request, 'diary/today_diary_detail.html', {'diary': diary})
    form = DiaryCreateForm()
    return render(request, 'diary/create_diary.html', {'Diary': form})

@login_required
def week_graph(request,selected_date=None):
    # selected_dateをdatetime.date型に変換
    if selected_date:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    # パラメータが指定されていない場合は今日の日付を使用
    else:
        selected_date = date.today()
    #Emotionのinstance化
    emotion = Emotion.objects.filter(user = request.user)
    # 選択された日付の曜日を取得
    selected_weekday = selected_date.weekday()
    # カレンダーの開始日を計算（選択された日の週の日曜日）
    start_of_week = selected_date - timedelta(days=(selected_weekday + 1) % 7)
    # カレンダーに表示する日付のリストを作成
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
    # 前の週の日曜日を取得
    week_start =week_dates[0]- timedelta(days=7)
    # 次の週の日曜日を取得
    week_start_up =week_dates[0]+ timedelta(days=7)
    # ユーザの日記を全て取得
    diary = Diary.objects.filter(user=request.user)
    #json形式で受け取る
    data = chart_data_week(request,start_of_week)
    chart_data_json = JsonResponse(data, safe=False).content.decode('utf-8')
    return render(request, 'diary/week_graph.html' ,{'week_dates': week_dates, 'selected_date': selected_date, 'diary':diary,'week_start':week_start,'week_start_up':week_start_up,'emotion':emotion,'data':chart_data_json})

def chart_data_day(request, pk):
    # Emotionデータをフィルタリング
    emotions = Emotion.objects.filter(user = request.user, diary_id=pk)  # または必要な条件に基づいてフィルタリング
    # データをJSON形式に変換
    data = {
        'labels': [emotion.reasoning for emotion in emotions],
        'positive': [emotion.positive for emotion in emotions],
        'negative': [emotion.negative for emotion in emotions],
        'neutral': [emotion.neutral for emotion in emotions],
        'mixed': [emotion.mixed for emotion in emotions],
    }
    return data

@login_required
def today_diary_graph(request, pk):
    # Diary モデルから特定の日記データを取得
    diary = get_object_or_404(Diary, id=pk)

    # Diary インスタンスから ai_comment を取得
    ai_comment = diary.ai_comment
    data = chart_data_day(request,pk)
    # JsonResponseを使用してJSONデータを返す
    circle_data_json=JsonResponse(data, safe=False).content.decode('utf-8')
    print(data)
    print(circle_data_json)
    return render(request,'diary/today_diary_graph.html',{'diary':diary, 'ai_comment':ai_comment, 'data':circle_data_json})

@login_required
def today_counseling_graph(request):
  return render(request,'diary/today_counseling_graph.html')

@login_required
def record_diary_detail(request):
  return render(request,'diary/record_diary_detail.html')

@login_required
def record_diary_graph(request):
  return render(request,'diary/record_diary_graph.html')

