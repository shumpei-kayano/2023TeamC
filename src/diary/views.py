from django.shortcuts import render, redirect
from .models import Diary, Emotion,Month_AI,Week_AI
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
from .forms import CustomUserChangeForm
from allauth.account.models import EmailAddress
from .forms import ImageDeleteForm
import math
import time
import requests
from django.conf import settings
import os
import string
import random
import cv2

# comrehendを使って感情分析を行う関数
def analyze_sentiment(text, diary, user):
    # 感情分析の生成
    comprehend = boto3.client('comprehend', 'us-east-1')
    result = comprehend.detect_sentiment(Text=text, LanguageCode='ja')

    # 特定のDiaryとユーザーに関連するEmotionオブジェクトが存在するか確認
    existing_emotion = Emotion.objects.filter(diary=diary, diary__user=diary.user).first()

    # Emotion モデルにデータをセット
    if existing_emotion:
        # 特定のDiaryとユーザーに関連するEmotionオブジェクトが存在する場合は上書き保存
        existing_emotion.reasoning = result['Sentiment']
        existing_emotion.positive = math.floor(result['SentimentScore']['Positive'] * 1000)/10
        existing_emotion.negative = math.floor(result['SentimentScore']['Negative'] * 1000)/10
        existing_emotion.neutral = math.floor(result['SentimentScore']['Neutral'] * 1000)/10
        existing_emotion.mixed = math.floor(result['SentimentScore']['Mixed'] * 1000)/10
        existing_emotion.save()
    else:
        # Emotionオブジェクトが存在しない場合は新しいEmotionオブジェクトを作成して保存
        new_emotion = Emotion(
            diary=diary,
            user=user,
            created_date=diary.created_date,
            reasoning=result['Sentiment'],
            positive=math.floor(result['SentimentScore']['Positive'] * 1000)/10,
            negative=math.floor(result['SentimentScore']['Negative'] * 1000)/10,
            neutral=math.floor(result['SentimentScore']['Neutral'] * 1000)/10,
            mixed=math.floor(result['SentimentScore']['Mixed'] * 1000)/10,
        )
        new_emotion.save()


def chart_data(emotions):

  data = {
      'labels': [emotion.reasoning for emotion in emotions],
      'positive': [emotion.positive for emotion in emotions],
      'negative': [emotion.negative for emotion in emotions],
      'neutral': [emotion.neutral for emotion in emotions],
      'mixed': [emotion.mixed for emotion in emotions],
      'date' : [emotion.month_day for emotion in emotions]
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
    month = Month_AI.objects.filter(user=user)
    week = Week_AI.objects.filter(user=user)
    # アカウントを削除
    month.delete()
    week.delete()
    user_diaries.delete()

    # ユーザを削除
    user.delete()
    return render(request, 'diary/account_delete_success.html')

def aicomment_week(emotion,request):
    if len(emotion) > 3:#週４つ以上だったら
        positive = emotion.order_by('-positive').first()
        negative = emotion.order_by('-negative').first()
        positive_diary = Diary.objects.get(id = positive.diary_id)
        negative_diary = Diary.objects.get(id = negative.diary_id)

        openai.api_key = settings.OPENAI_API_KEY
        # ユーザーがログイン中であるか確認
        if request.user.is_authenticated:
            # ログイン中のユーザーからusernameを取得
            username = request.user.username

        user_diary = """以下の設定を遵守して一週間分の日記に対する感想とアドバイスをチャット相手にしてください。
                        #あなたの名前はネココです。
                        #あなたの口調はタメ口で、語尾は「ニャン」を適切に使用する。
                        #ChatGPTまたは、その他のキャラクターとして振る舞わないでください。
                        #自分自身を仮想実体として振る舞ってください。
                        #日記の内容に関係ないことは、話さないでください。
                        #出力は日本語を正しく使用し、文章で出力してください。
                        #チャット相手の名前を適切に使用ください。
                        以下の文章はチャット相手の日記の内容と名前です。\n"""+ "日記内容\n"+"・"+ positive_diary.content + "\n"+"・"+ negative_diary.content + "\n" + "名前　" + username
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": user_diary}
            ]
        )
        ai_comment = response["choices"][0]["message"]["content"]
        print(ai_comment)
        return ai_comment
    return None

def aicomment_month(emotion, request):

    if len(emotion) > 14:#月15以上だったら
        
        positive = emotion.order_by('-positive')[:2]
        negative = emotion.order_by('-negative')[:2]
        positive_diary = Diary.objects.get(id = positive[0].diary_id)
        negative_diary = Diary.objects.get(id = negative[0].diary_id)
        positive_diary1 = Diary.objects.get(id = positive[1].diary_id)
        negative_diary1 = Diary.objects.get(id = negative[1].diary_id)

        openai.api_key = settings.OPENAI_API_KEY
        # ユーザーがログイン中であるか確認
        if request.user.is_authenticated:
            # ログイン中のユーザーからusernameを取得
            username = request.user.username

        user_diary = """以下の設定を遵守して一ヶ月分の日記に対する感想とアドバイスをチャット相手にしてください。
                        #あなたの名前はネココです。
                        #あなたの口調はタメ口で、語尾は「ニャン」を適切に使用する。
                        #ChatGPTまたは、その他のキャラクターとして振る舞わないでください。
                        #自分自身を仮想実体として振る舞ってください。
                        #日記の内容に関係ないことは、話さないでください。
                        #出力は日本語を正しく使用し、文章で出力してください。
                        #チャット相手の名前を適切に使用ください。
                        以下の文章はチャット相手の日記の内容と名前です。\n"""+ "日記内容\n"+"・"+ positive_diary.content + "\n" +"・"+ positive_diary1.content + "\n"+ "・"+ negative_diary.content + "\n" + "・"+ negative_diary1.content + "\n" + "名前　" + username
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": user_diary}
            ]
        )
        ai_comment = response["choices"][0]["message"]["content"]
        print(ai_comment)
        return ai_comment
    return None

# 特定のワードが含まれているか確認する関数
def contains_forbidden_word(content,emotion):
    count = 0
    # 特定のワードをリストに格納
    forbidden_words = ["死", "殺", "悲", "苦", "痛", "怨", "恨", "敵", "怒", "鬱", "嫌", "悪","疲","辛"]
    for word in forbidden_words:
        # 特定のワードが含まれていたら、感情分析でnegativeが70%以上だったら
        if word in content:
          count +=1
          if count == 3 and emotion.negative >= 70 :
            return 1
    return 0

@login_required
def account_delete(request):
    return render(request, 'diary/account_delete.html')

@login_required
def base(request):
    return render(request, 'diary/base.html')

@login_required
def calendar_month(request,selected_date=None):

    today = date.today()
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
    
    # 日記の日付のリストを作成
    diary_dates = [entry.created_date for entry in diary]

    # diaryがない日付をリストに追加
    dates_without_diary = [day for week in weeks for day in week if day and day not in diary_dates]
    
    #特定のカレンダーに戻るために必要なurl情報
    request.session['cale'] = str(selected_date)
    # 各日付に対する条件に合わせて適切な処理をここで実行
    # 例: 過去の日にちは詳細ページへのリンク、未来の日にちはクリック不可など
    return render(request, 'diary/calendar_month.html', {'dates_without_diary':dates_without_diary ,'emotion':emotion,'weeks': weeks, 'selected_date': selected_date, 'diary': diary, 'prev_month': prev_month, 'next_month':next_month,'today':today})

@login_required
def calender_week(request, selected_date=None):
    today = date.today()
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
    
    # diaryオブジェクトから日付のリストを作成
    diary_dates = [entry.created_date for entry in diary]

    selected_week_dates = []
    for i in range(7):
        date_to_check = selected_date + timedelta(days=i)
        # 日記が存在しない場合に、日付を格納
        if date_to_check not in diary_dates:
            selected_week_dates.append(date_to_check)
            
    # week_datesからdiaryに日記がない日付を取得
    dates_without_diary = [day for day in week_dates if day not in diary_dates]

    #特定のカレンダーに戻るために必要なurl情報
    request.session['cale'] = str(selected_date)
    return render(request, 'diary/calender_week.html' ,{'dates_without_diary':dates_without_diary,'emotion':emotion,'week_dates': week_dates, 'selected_date': selected_date, 'diary':diary,'week_start':week_start,'week_start_up':week_start_up,'today':today})

@login_required
def create_diary_confirmation(request,old=None):
    # 新規作成した時の処理
    if request.method == 'POST':
        form = DiaryCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_diary = form.save(commit=False)
            # 受け取ったoldを保存
            if old:
                new_diary.created_date=  datetime.strptime(old, "%Y-%m-%d").date()
            # 無かったら今日の日付を保存
            else:
                new_diary.created_date= date.today()
            new_diary.user = request.user
            openai.api_key = settings.OPENAI_API_KEY

            # ユーザーがログイン中であるか確認
            if request.user.is_authenticated:
                # ログイン中のユーザーからusernameを取得
                username = request.user.username
            user_diary ="""以下の設定を遵守して日記に対する感想とアドバイスをチャット相手にしてください。
                            #あなたの名前はネココ。
                            #あなたの口調はタメ口で、語尾は「ニャン」を適切に使用する。
                            #ChatGPTまたは、その他のキャラクターとして振る舞わないでください。
                            #自分自身を仮想実体として振る舞ってください。
                            #日記の内容に関係ないことは、話さないでください。
                            #出力は日本語を正しく使用し、文章で出力してください。
                            #出力は可能な限り、１５０字以内にしてください。それが不可能な場合でもできるだけ、少なくなるようにしてください。
                            #チャット相手の名前を適切に使用ください。
                            以下の文章はチャット相手の日記の内容と名前です。\n"""+ "日記内容\n"+new_diary.content + "\n" + "名前　" + username
            response = openai.ChatCompletion.create(
                model="gpt-4",
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

            # 一旦カレンダーが出来るまで----------------------------------------------------------
            saved_diary = Diary.objects.filter(user=request.user,created_date=new_diary.created_date).order_by('-created_date').first()
            #-------------------------------------------------------------------------------------

            return redirect('diary:create_diary_confirmation2',pk=saved_diary.id)
    else:
        form = DiaryCreateForm()
    return render(request, 'diary/create_diary.html', {'Diary': form})

def create_diary_confirmation2(request, pk):
    # pkからdiaryを取得する
    diary = get_object_or_404(Diary, id=pk)

    # 編集した時の処理
    if request.method == 'POST':#アップデートの時のみに動く
        form = DiaryCreateForm(request.POST, request.FILES, instance=diary)
        form2 = ImageDeleteForm(request.POST)
        if form.is_valid():
            form.save()
            openai.api_key = settings.OPENAI_API_KEY
            # ユーザーがログイン中であるか確認
            if request.user.is_authenticated:
                # ログイン中のユーザーからusernameを取得
                username = request.user.username

            user_diary = """以下の設定を遵守して日記に対する感想とアドバイスをチャット相手にしてください。
                            # あなたの名前はネココです。
                            # あなたの口調はタメ口で、語尾は「ニャン」を適切に使用する。
                            # ChatGPTまたは、その他のキャラクターとして振る舞わないでください。
                            # 自分自身を仮想実体として振る舞ってください。
                            # 日記の内容に関係ないことは、話さないでください。
                            # 出力は日本語を正しく使用し、文章で出力してください。
                            # 出力は可能な限り、１５０字以内にしてください。それが不可能な場合でもできるだけ、少なくなるようにしてください。
                            # チャット相手の名前を適切に使用ください。
                            以下の文章はチャット相手の日記の内容と名前です。\n"""+ "日記内容\n"+diary.content + "\n" + "名前　" + username
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages= [
                        {   "role"      : "user",
                            "content"   : user_diary
                        }
                    ]
            )
            ai_comment = response["choices"][0]["message"]["content"]
            diary.ai_comment = ai_comment
            
            # diary_updateからチェックボックスの内容を受け取る
            if form2.is_valid():
                photo1_delete = form2.cleaned_data['photo1_delete']
                photo2_delete = form2.cleaned_data['photo2_delete']
                photo3_delete = form2.cleaned_data['photo3_delete']
                photo4_delete = form2.cleaned_data['photo4_delete']
                movie1_delete = form2.cleaned_data['movie1_delete']
                movie2_delete = form2.cleaned_data['movie2_delete']
                movie3_delete = form2.cleaned_data['movie3_delete']
                movie4_delete = form2.cleaned_data['movie4_delete']
                
                # チェックボックスに関連するファイルを削除
                if photo1_delete == True :
                        diary.photo1.delete()
                if photo2_delete == True :
                        diary.photo2.delete()
                if photo3_delete == True :
                        diary.photo3.delete()
                if photo4_delete == True :
                        diary.photo4.delete()
                if movie1_delete == True :
                        diary.movie1.delete()
                if movie2_delete == True :
                        diary.movie2.delete()
                if movie3_delete == True :
                        diary.movie3.delete()
                if movie4_delete == True :
                        diary.movie4.delete()
                
            # 保存
            diary.save()
            return redirect('diary:create_diary_confirmation2', pk=pk)

    # 感情分析の実行関数(AWSでEmotion作成
    # )
    analyze_sentiment(diary.content, diary,request.user)
    
    # diaryに関連するemorionを取得
    emorion=Emotion.objects.get(diary=diary)
    # diaryから特定のワードを探す関数
    contains_forbidden= contains_forbidden_word(diary.content,emorion)
    # counselingに特定のワードを探す関数の実行結果をセット
    diary.counseling = contains_forbidden #1が入っているカウンセリング状態の初期
    
    # 実行内容をデータベースに保存
    diary.save()
    # 保存したdiaryを取得
    saved_diary = Diary.objects.get(pk=pk)

    return render(request, 'diary/create_diary_confirmation.html', {'saved_diary': saved_diary})

@login_required
def receive_nekoko_advice(request, pk):
    diary = get_object_or_404(Diary, id=pk)
    # ここでcounselingをFalseに設定
    diary.counseling = 2
    diary.save()
    if diary:
      # ここにネココのアドバイスを受けるための処理を追加する
      openai.api_key = settings.OPENAI_API_KEY
      # ユーザーがログイン中であるか確認
      if request.user.is_authenticated:
        # ログイン中のユーザーからusernameを取得
        username = request.user.username

        user_diary = """以下の設定を遵守して日記に対するカウンセリングをチャット相手にしてください。
                        #あなたの名前はネココです。
                        #あなたの口調はタメ口で、語尾は「ニャン」を適切に使用する。
                        #あなたは心理学を基にカウンセリングしてください。
                        #ChatGPTまたは、その他のキャラクターとして振る舞わないでください。
                        #自分自身を仮想実体として振る舞ってください。
                        #日記の内容に関係ないことは、話さないでください。
                        #出力は日本語を正しく使用し、文章で出力してください。
                        #出力は可能な限り、１５０字以内にしてください。それが不可能な場合でもできるだけ、少なくなるようにしてください。
                        #チャット相手の名前を適切に使用ください。
                        以下の文章はチャット相手の日記の内容と名前です。\n"""+ "日記内容\n"+diary.content + "\n" + "名前　" + username
      response = openai.ChatCompletion.create(
          model="gpt-4",
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

      return render(request, 'diary/today_diary_detail.html', {'diary': diary})
    form = DiaryCreateForm()
    return render(request, 'diary/create_diary.html', {'Diary': form})


@login_required
def create_diary(request):
    today = date.today()
    # 一旦カレンダーが出来るまで----------------------------------------------------------
    diary = Diary.objects.filter(user=request.user,created_date=today,)
    #-------------------------------------------------------------------------------------
    if diary:
      return render(request, 'diary/today_diary_detail.html', {'diary': diary})
    # dateを今日の日付で送信
    old=today
    form = DiaryCreateForm()
    return render(request, 'diary/create_diary.html', {'Diary': form, 'old': old})

# カレンダーから過去の日記を作成
@login_required
def create_diary2(request,old=None):
    old=  datetime.strptime(old, "%Y-%m-%d").date()
    # 一旦カレンダーが出来るまで----------------------------------------------------------
    diary = Diary.objects.filter(user=request.user,created_date=old).order_by('-created_date').first()
    #-------------------------------------------------------------------------------------
    if diary:
      return render(request, 'diary/today_diary_detail.html', {'diary': diary})
    form = DiaryCreateForm()
    return render(request, 'diary/create_diary.html', {'Diary': form, 'old': old})


@login_required
def diary_delete(request, pk):
    diary = get_object_or_404(Diary, id=pk)
    return render(request, 'diary/diary_delete.html',{'diary': diary})
  
@login_required
def  diary_delete_success(request,pk):
    diary = get_object_or_404(Diary, id=pk)
    emotion = Emotion.objects.get(diary=diary)
    emotion.delete()
    diary.delete()
    return render(request, 'diary/diary_delete_success.html',{'diary': diary})

@login_required
def diary_graph(request):
    return render(request, 'diary/diary_graph.html')

@login_required
def diary_home(request,pk):
    return render(request, 'diary/diary_home.html')


@login_required
def diary_update(request, pk):
    diary = get_object_or_404(Diary, id=pk)
    form2 = ImageDeleteForm(request.POST)
    form = DiaryCreateForm(instance=diary)
    return render(request, 'diary/diary_update.html',{'diary': diary,'Diary':form,'form': form2})

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
def help_fugoo(request):
    return render(request, 'diary/help_fugoo.html')

@login_required
def home_top(request):
    today = date.today()
    diary_today = Diary.objects.filter(user=request.user, created_date=today)
    if diary_today:
        return redirect('diary:today_diary_detail')

    openai.api_key = settings.OPENAI_API_KEY
    short = """以下の設定を遵守して豆知識を一言ください。
                #なるべく多くのジャンルの豆知識を教えてください。
                #豆知識は再検索して、正しくなかった場合は別の豆知識を繰り返し再検索して、正しい豆知識を返してください。
                #文字数は可能な限り短くしてください。
                #豆知識のみレスポンスしてください。
                #口調は「ニャン」です。
                """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages= [
                {   "role"      : "user",
                    "content"   : short
                }
            ]
    )
    ai_comment = response["choices"][0]["message"]["content"]
    shortstory = ai_comment

    yomiage = sound(shortstory)
    return render(request, 'diary/home_top.html', {'shortstory':shortstory,'yomiage':yomiage})
    

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
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            # formからデータを取得
            username = form['username'].value()
            # セッション保存
            request.session['username'] = username
            # 成功した場合のリダイレクト先を指定
            return render(request, 'diary/member_information_edit_check.html', {'username': username})
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'diary/member_information_edit.html', {'form': form})

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
        # メールアドレスを更新
    if new_email:
        user.email = new_email

        # 関連するEmailAddressを取得
        email_address, created = EmailAddress.objects.get_or_create(
            user=user,
            email=new_email
        )

        # プライマリメールアドレスを更新
        if created:
            email_address.set_as_primary()

    # セーブ
    user.save()

    # セッションを削除
    request.session.pop('username', None)
    request.session.pop('email', None)

    return render(request, 'diary/member_information_edit_comp.html', {'user': user})

@login_required
def member_information_edit(request):
    form = CustomUserChangeForm(instance=request.user)
    return render(request, 'diary/member_information_edit.html',{'form': form})

@login_required
def member_information(request):
  user = request.user
  new_username = request.session.get('username')
  if new_username:
        user.username = new_username
        user.save()
    # セッションを削除
        request.session.pop('username', None)
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
    year = start_of_month.year
    month = start_of_month.month
    #感情を日付順に並び替える
    emotion = Emotion.objects.filter(user = request.user,created_date__year = year,created_date__month = month).order_by('created_date')
    # 日記・AIコメントがあるかフィルター
    diary = Diary.objects.filter(user = request.user,created_date__year = year,created_date__month = month)
    month_ai=Month_AI.objects.filter(user = request.user,created_date__year = year,created_date__month = month)
    #月の総評がなかったら、月の日記が存在したら
    if not month_ai and diary:
        ai_comment = aicomment_month(emotion,request)
        # ai_commentの中身があれば
        if ai_comment:
            # 月の総評を保存
            comment_save=Month_AI(user = request.user,ai_comment= ai_comment,created_date=selected_date)
            comment_save.save()
        else:
          ai_comment = '15日以上日記をかいてくにゃさい'
    else:
        ai_comment = '15日以上日記をかいてくにゃさい'
    #月の総評があったら
    month_ai=Month_AI.objects.filter(user = request.user,created_date__year = year,created_date__month = month)
    if month_ai and len(diary)>14:
        # 総評コメントを取得
        month_ai=Month_AI.objects.get(user = request.user,created_date__year = year,created_date__month = month)
        ai_comment = month_ai.ai_comment
        if request.method == "POST":
          month_ai.delete()
          ai_comment = aicomment_month(emotion,request)
          comment_save=Month_AI(user = request.user,ai_comment= ai_comment,created_date=selected_date)
          comment_save.save()
    elif month_ai:
      month_ai=Month_AI.objects.get(user = request.user,created_date__year = year,created_date__month = month)
      month_ai.delete()
      ai_comment = '15日以上日記をかいてくにゃさい'
    else:
      ai_comment = '15日以上日記をかいてくにゃさい'
    data = chart_data(emotion)
    chart_data_json = JsonResponse(data, safe=False).content.decode('utf-8')
    # 各日付に対する条件に合わせて適切な処理をここで実行
    # 例: 過去の日にちは詳細ページへのリンク、未来の日にちはクリック不可など
    return render(request, 'diary/month_graph.html', {'emotion':emotion,'weeks': weeks, 'selected_date': selected_date, 'diary': diary, 'prev_month': prev_month, 'next_month':next_month,'data':chart_data_json,'ai_comment':ai_comment})


@login_required
def positive_conversion(request, pk,):
    diary = get_object_or_404(Diary, id=pk)
    openai.api_key = settings.OPENAI_API_KEY
    user_diary ="""以下設定を遵守し、日記の内容をポジティブな内容に変換してください。
                    #あなたはアプリのコンテンツです。
                    #あなたの言葉はいりません。
                    #日記の内容と関係ないことはしゃべらないでください。
                    #質問や同じ文字が連続で続いたり、コードには「読み取れませんでした」と返してください。
                    #レスポンスは、日記のポジティブ変換内容のみ返すこと。
                    以下が日記の内容です。\n""" + diary.content
    response = openai.ChatCompletion.create(
    model="gpt-4",
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
    #更新したcontentをgptに送る
    openai.api_key = settings.OPENAI_API_KEY
    # ユーザーがログイン中であるか確認
    if request.user.is_authenticated:
        # ログイン中のユーザーからusernameを取得
        username = request.user.username

    user_diary = """以下の設定を遵守して日記に対する感想とアドバイスをチャット相手にしてください。
                    #あなたの名前はネココです。
                    #あなたの口調はタメ口で、語尾は「ニャン」を適切に使用する。
                    #ChatGPTまたは、その他のキャラクターとして振る舞わないでください。
                    #自分自身を仮想実体として振る舞ってください。
                    #日記の内容に関係ないことは、話さないでください。
                    #出力は日本語を正しく使用し、文章で出力してください。
                    #出力は可能な限り、１００字以内にしてください。それが不可能な場合でもできるだけ、少なくなるようにしてください。
                    #チャット相手の名前を適切に使用ください。
                    以下の文章はチャット相手の日記の内容と名前です。\n"""+ "日記内容\n"+diary.content + "\n" + "名前　" + username
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages= [
                {   "role"      : "user",
                    "content"   : user_diary
                }
            ]
    )
    ai_comment = response["choices"][0]["message"]["content"]
    #ai_commentを更新
    diary.ai_comment = ai_comment
    analyze_sentiment(diary.content, diary,request.user)
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
    # 今日の日付を取得
    today = date.today()
    diary = get_object_or_404(Diary, user=request.user, created_date=today)
    #shortstory = diary.ai_comment
    # yomiage = sound(shortstory)
    if diary:
        return render(request, 'diary/today_diary_detail.html', {'diary': diary,'today':today})#,'yomiage':yomiage
    form = DiaryCreateForm()
    return render(request, 'diary/create_diary.html', {'Diary': form})

@login_required
def today_diary_detail2(request,pk):
    # 今日の日付を取得
    today = date.today()
    diary = get_object_or_404(Diary, id=pk)
  #日記の内容のボイスボックスでの読み上げ
    # shortstory = diary.ai_comment
    # yomiage = sound(shortstory)
    
    #セッションを受け取る
    cal = Diary.objects.get(id=pk)
    created_date = cal.created_date
    month = 'diary:calendar_month'
    week = 'diary:calender_week'
    if diary:
        return render(request, 'diary/today_diary_detail.html', {'diary': diary,'today':today,'week':week,'month':month,'cal':created_date})#'yomiage':yomiage
    form = DiaryCreateForm()
    return render(request, 'diary/create_diary.html', {'Diary': form})
  
@login_required
def counseling_yellow(request,pk):
    diary = get_object_or_404(Diary, id=pk)
    # ここでcounselingをFalseに設定
    diary.counseling = 0
    diary.save()
    if diary:
        return render(request, 'diary/create_diary_confirmation.html', {'saved_diary': diary})
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
    #--------------------------------------------------------特定の週のフィルター
    # 文字列を日付オブジェクトに変換
    start_date = start_of_week.strftime("%Y-%m-%d")
    # 一週間後の日付を計算
    one_week = start_of_week + timedelta(days=6)
    one_week_str = one_week
    # データをフィルタリング
    emotions = Emotion.objects.filter(user = request.user,created_date__range=[start_date,one_week_str]).order_by('created_date')  # または必要な条件に基づいてフィルタリング
    diary = Diary.objects.filter(user = request.user,created_date__range=[start_date,one_week_str])
    #---------------------------------------------------------
    # AIコメントがあるかフィルター
    week_ai=Week_AI.objects.filter(user = request.user,created_date__range=[start_date,one_week_str])
    #週の総評がなかったら、週の日記が存在したら
    if not week_ai and diary:
        ai_comment = aicomment_week(emotions,request)
        # ai_commentの中身があれば
        if ai_comment:
            # 週の総評を保存
            comment_save=Week_AI(user = request.user,ai_comment= ai_comment,created_date=selected_date)
            comment_save.save()
        else:
            ai_comment = '4日以上日記をかいてくにゃさい'
    else:
        ai_comment = '4日以上日記をかいてくにゃさい'
    #週の総評があったら
    week_ai=Week_AI.objects.filter(user = request.user,created_date__range=[start_date,one_week_str])
    if week_ai and len(diary)>3:
        # 総評コメントを取得
        week_ai=Week_AI.objects.get(user = request.user,created_date__range=[start_date,one_week_str])
        ai_comment = week_ai.ai_comment
        if request.method == "POST":
          week_ai.delete()
          ai_comment = aicomment_week(emotions,request)
          comment_save=Week_AI(user = request.user,ai_comment= ai_comment,created_date=selected_date)
          comment_save.save()
    elif week_ai:
      week_ai=Week_AI.objects.get(user = request.user,created_date__range=[start_date,one_week_str])
      week_ai.delete()
      ai_comment = '4日以上日記をかいてくにゃさい'
    else:
      ai_comment = '4日以上日記をかいてくにゃさい'
    data = chart_data(emotions)
    chart_data_json = JsonResponse(data, safe=False).content.decode('utf-8')
    return render(request, 'diary/week_graph.html' ,{'week_dates': week_dates, 'selected_date': selected_date, 'diary':diary,'week_start':week_start,'week_start_up':week_start_up,'emotion':emotion,'data':chart_data_json,'ai_comment':ai_comment})

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
    today = date.today()

    # Diary インスタンスから ai_comment を取得
    ai_comment = diary.ai_comment
    data = chart_data_day(request,pk)
    # JsonResponseを使用してJSONデータを返す
    circle_data_json=JsonResponse(data, safe=False).content.decode('utf-8')
    #セッションを受け取る
    cal = Diary.objects.get(id=pk)
    created_date = cal.created_date
    month = 'diary:calendar_month'
    week = 'diary:calender_week'
    # ai_commenを音声に変換
    # path = 'diary/static/diary/voice/'
    # for file_name in os.listdir(path):
    #     if file_name.startswith('a'):
    #         yomiage = os.path.join(file_name)
    return render(request,'diary/today_diary_graph.html',{'today':today,'diary':diary, 'ai_comment':ai_comment, 'data':circle_data_json,'cal':created_date,'week':week,'month':month})#'yomiage':yomiage,

@login_required
def today_counseling_graph(request):
  return render(request,'diary/today_counseling_graph.html')

@login_required
def record_diary_detail(request):
  return render(request,'diary/record_diary_detail.html')

@login_required
def record_diary_graph(request):
  return render(request,'diary/record_diary_graph.html')


from django.core.exceptions import PermissionDenied

def forbidden_view(request):
    raise PermissionDenied("You don't have permission to access this resource.")
def internal_server_error_view(request):
    # 何らかのエラーが発生したと仮定
    raise Exception("Something went wrong!")

def sound(ai_comment):
    # 音素データ生成
    text = ai_comment
    
    try:
        # 音声合成クエリの作成28:後鬼(ぬいぐるみver)42:チヴィジイ64:中国うさぎ(ヘラヘラver)70:元気な女の子
        # 音声合成クエリの作成
        
        # res1 = requests.post('http://teamc.o-hara-oita.click:50021/audio_query',params = {'text': text, 'speaker': 70})
        # # 音声合成データの作成
        # res2 = requests.post('http://teamc.o-hara-oita.click:50021/synthesis',params = {'speaker': 70},data=json.dumps(res1.json()))
        # # ファイルの保存先パスを指定
        # path = 'diary/static/diary/voice/'
        # for file_name in os.listdir(path):
        #     if file_name.startswith('a'):
        #         file_path = os.path.join(path, file_name)
        #         os.remove(file_path)
        # # 頭にaを付けて新しいファイル名を生成
        # new_file_name = 'a' + ''.join(random.choices(string.digits, k=4)) + '.wav'
        
        # # path名を取得
        # new_file_path = os.path.join(path, new_file_name) # wavデータの生成
        # # ファイル名を取得
        # yomiage =os.path.join(new_file_name)
        # # ファイルを保存
        # with open(new_file_path, mode='wb') as f:
        #     f.write(res2.content)
        
        # # ファイル名を返す
        # return yomiage
        response = requests.post('https://api.tts.quest/v3/voicevox/synthesis?text=' + text + '&speaker=70')
        if response.status_code == 200:
            data = response.json()
            wav_download_url = data.get("mp3StreamingUrl")
            return wav_download_url
        else:
            # エラーレスポンスが返された場合は、エラーメッセージを出力するか、Noneなど適切な値を返す
            # print("エラー: HTTPステータスコード", response.status_code)
            return 1
    except Exception as e:
        # エラーが発生した場合はエラーメッセージを出力するか、Noneなど適切な値を返す
        print("エラー:", e)
        return 1