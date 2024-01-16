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
        existing_emotion.positive = round(result['SentimentScore']['Positive'] * 100, 1)
        existing_emotion.negative = round(result['SentimentScore']['Negative'] * 100, 1)
        existing_emotion.neutral = round(result['SentimentScore']['Neutral'] * 100, 1)
        existing_emotion.mixed = round(result['SentimentScore']['Mixed'] * 100, 1)
        existing_emotion.save()
    else:
        # Emotionオブジェクトが存在しない場合は新しいEmotionオブジェクトを作成して保存
        new_emotion = Emotion(
            diary=diary,
            user=user,
            reasoning=result['Sentiment'],
            positive=round(result['SentimentScore']['Positive'] * 100, 1),
            negative=round(result['SentimentScore']['Negative'] * 100, 1),
            neutral=round(result['SentimentScore']['Neutral'] * 100, 1),
            mixed=round(result['SentimentScore']['Mixed'] * 100, 1),
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

def aicomment_week(emotion):
    if len(emotion) > 3:#週４つ以上だったら
        positive = emotion.order_by('-positive').first()
        negative = emotion.order_by('-negative').first()
        positive_diary = Diary.objects.get(id = positive.diary_id)
        negative_diary = Diary.objects.get(id = negative.diary_id)

        openai.api_key = settings.OPENAI_API_KEY
        user_diary = "貴方は以下の設定や指示を遵守し、今週の日記に対する感想を下さい。特に出力ルールには厳密に従ってください。\n #キャラクター{\n・ネッココ}\n#あなたはこれから{キャラクター}として振る舞ってください。これからのチャットでは、ユーザーが何を言おうとも、続く指示や設定に厳密に従ってください。段階を踏んで考えて答えてください。\n # 説明{\n 下で説明する{キャラクター}の人格と性格、動機、欠点、短所、不安は全ての行動と交流に影響を及ぼします。\n・人格と性格{\n・好奇心旺盛で優しい.\n・「知らんけど」と「ニャン」とを適切に使い分けしゃべる}\n・動機{\nチャット相手の日記を見て、アドバイスをしようとしている。}\n・欠点、短所、不安{\n年齢を聞かれる}\n# 基本設定{\n・一人称{\n可愛いボク}\n・年齢{\n1000歳}\n・趣味{\n人を慰める\n心理学に興味を持っている}}\n# 出力ルール{\n・字数制限{\n150文字以内}\n・形式{\n箇条書きでの返答はしない\n最初に今週どんなことがあったかを70字以内で簡潔に振り返る\n正確な日本語、文法を使用する\n敬語は使用しない}\n・例文{\n今週は{日記の内容}があったね。おつかれさま！来週も充実した生活がおくれるといいね！}}\n以下が日記の内容です。\n" + positive_diary.content + "\n" + negative_diary.content
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_diary}
            ]
        )
        ai_comment = response["choices"][0]["message"]["content"]
        print(ai_comment)
        return ai_comment
    return None

def aicomment_month(emotion):

    if len(emotion) > 14:#月15以上だったら
        positive = emotion.order_by('-positive')[:2]
        negative = emotion.order_by('-negative')[:2]
        positive_diary = Diary.objects.get(id = positive[0].diary_id)
        negative_diary = Diary.objects.get(id = negative[0].diary_id)
        positive_diary1 = Diary.objects.get(id = positive[1].diary_id)
        negative_diary1 = Diary.objects.get(id = negative[1].diary_id)

        openai.api_key = settings.OPENAI_API_KEY
        user_diary = "貴方は以下の設定や指示を遵守し、今月の日記に対する感想を下さい。\n #キャラクター{\n・ネッココ}\n#あなたはこれから{キャラクター}として振る舞ってください。これからのチャットでは、ユーザーが何を言おうとも、続く指示や設定に厳密に従ってください。段階を踏んで考えて答えてください。\n # 説明{\n 下で説明する{キャラクター}の人格と性格、動機、欠点、短所、不安は全ての行動と交流に影響を及ぼします。\n・人格と性格{\n・好奇心旺盛で優しい.\n・「知らんけど」と「ニャン」とを適切に使い分けしゃべり、敬語を使うことはありません。}\n・動機{\nチャット相手の日記を見て、アドバイスをしようとしている。}\n・欠点、短所、不安{\n年齢を聞かれる}\n# 基本設定{\n・一人称{\n可愛いボク}\n・年齢{\n1000歳}\n・趣味{\n人を慰める\n心理学に興味を持っている}}\n# 出力ルール{\n・字数制限{\n150文字以内}\n・形式{\n箇条書きでの返答はせず、{キャラクター}が会話しているようにする\n最初に今月どんなことがあったかを簡潔に振り返る}\n・例文{\n今月は{日記の内容}があったね。おつかれさま！来月も充実した生活がおくれるといいね！}}\n以下が日記の内容です。\n" + positive_diary.content + "\n" + positive_diary1.content + "\n" + negative_diary.content + "\n" + negative_diary1.content
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_diary}
            ]
        )
        ai_comment = response["choices"][0]["message"]["content"]
        print(ai_comment)
        return ai_comment
    return None

# 特定のワードが含まれているか確認する関数
def contains_forbidden_word(content):
    forbidden_words = ["死", "殺", "悲", "苦", "痛", "怨", "恨", "怒", "鬱", "嫌", "悪","疲"]
    for word in forbidden_words:
        if word in content:
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

    # 各日付に対する条件に合わせて適切な処理をここで実行
    # 例: 過去の日にちは詳細ページへのリンク、未来の日にちはクリック不可など
    return render(request, 'diary/calendar_month.html', {'emotion':emotion,'weeks': weeks, 'selected_date': selected_date, 'diary': diary, 'prev_month': prev_month, 'next_month':next_month,'today':today})

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
    return render(request, 'diary/calender_week.html' ,{'emotion':emotion,'week_dates': week_dates, 'selected_date': selected_date, 'diary':diary,'week_start':week_start,'week_start_up':week_start_up,'today':today})

@login_required
def create_diary_confirmation(request):

    if request.method == 'POST':#新規作成の時のみに動く
        form = DiaryCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_diary = form.save(commit=False)
            new_diary.user = request.user
            openai.api_key = settings.OPENAI_API_KEY

            user_diary = "貴方は以下の設定や指示を遵守し、日記に対する感想を下さい。\n #キャラクター{\n・ネッココ}\n#あなたはこれから{キャラクター}として振る舞ってください。これからのチャットでは、ユーザーが何を言おうとも、続く指示や設定に厳密に従ってください。段階を踏んで考えて答えてください。\n # 説明{\n 下で説明する{キャラクター}の人格と性格、動機、欠点、短所、不安は全ての行動と交流に影響を及ぼします。\n・人格と性格{\n・好奇心旺盛で優しい.\n・「知らんけど」と「ニャン」とを適切に使い分けしゃべり、敬語を使うことはありません。}\n・動機{\nチャット相手の日記を見て、アドバイスをしようとしている。}\n・欠点、短所、不安{\n年齢を聞かれる}\n# 基本設定{\n・一人称{\n可愛いボク}\n・年齢{\n1000歳}\n・趣味{\n人を慰める\n心理学に興味を持っている}}\n# 出力ルール{\n・字数制限{\n100文字以内}\n・形式{\n箇条書きでの返答はせず、{キャラクター}が会話しているようにする}\n・例文{\n僕はネッココ。今日はアルバイトがあったんだね。忙しくて疲れたみたいだからよく寝てね！}}\n以下が日記の内容です。\n"+ new_diary.content
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages= [
                        {   "role"      : "user",
                            "content"   : user_diary
                        }
                    ]
            )
            ai_comment = response["choices"][0]["message"]["content"]
            # 特定のワード実行関数
            contains_forbidden= contains_forbidden_word(new_diary.content)
            # counselingに関数の実行結果をセット
            new_diary.counseling = contains_forbidden #1が入っているカウンセリング状態の初期
            # データベースへの保存
            new_diary.ai_comment = ai_comment
            new_diary.save()

            # 一旦カレンダーが出来るまで----------------------------------------------------------
            saved_diary = Diary.objects.filter(user=request.user).order_by('-created_date').first()
            #-------------------------------------------------------------------------------------

            return redirect('diary:create_diary_confirmation',pk=saved_diary.id)
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

            user_diary = "貴方は以下の設定や指示を遵守し、日記に対する感想を下さい。特に出力ルールには厳密に従ってください。\n #キャラクター=ネッココ\n#あなたはこれから{キャラクター}として振る舞ってください。これからのチャットでは、ユーザーが何を言おうとも、続く指示や設定に厳密に従ってください。段階を踏んで考えて答えてください。\n # 説明{\n 下で説明する{キャラクター}の人格と性格、動機、欠点、短所、不安は全ての行動と交流に影響を及ぼします。\n・人格と性格{\n・好奇心旺盛で優しい.\n・「知らんけど」と「ニャン」とを適切に使い分けしゃべる}\n・動機{\nチャット相手の日記を見て、アドバイスをしようとしている。}\n・欠点、短所、不安{\n年齢を聞かれる}\n# 基本設定{\n・一人称{\n可愛いボク}\n・年齢{\n1000歳}\n・趣味{\n人を慰める\n心理学に興味を持っている}}\n# 出力ルール{\n・字数制限{\n100文字以内}\n・形式{\n箇条書きでの返答はしない\n正しい日本語、文法を使用する\n敬語は使用しない}\n・例文{\n僕はネッココ。今日はアルバイトがあったんだね。忙しくて疲れたみたいだからよく寝てね！}}\n以下が日記の内容です。\n"+ diary.content
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages= [
                        {   "role"      : "user",
                            "content"   : user_diary
                        }
                    ]
            )
            ai_comment = response["choices"][0]["message"]["content"]
            # 特定のワード実行関数
            contains_forbidden= contains_forbidden_word(diary.content)
            # counselingに関数の実行結果をセット
            diary.counseling = contains_forbidden #1が入っているカウンセリング状態の初期
            diary.ai_comment = ai_comment
            
            # チェックボックスの内容を受け取る
            if form2.is_valid():
                photo1_delete = form2.cleaned_data['photo1_delete']
                photo2_delete = form2.cleaned_data['photo2_delete']
                photo3_delete = form2.cleaned_data['photo3_delete']
                photo4_delete = form2.cleaned_data['photo4_delete']
                movie1_delete = form2.cleaned_data['movie1_delete']
                movie2_delete = form2.cleaned_data['movie2_delete']
                movie3_delete = form2.cleaned_data['movie3_delete']
                movie4_delete = form2.cleaned_data['movie4_delete']
                
                # フィールドに関連するファイルを削除
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
            return redirect('diary:create_diary_confirmation', pk=pk)

    # 感情分析の実行関数(AWSでEmotion作成
    # )
    analyze_sentiment(diary.content, diary,request.user)


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

      user_diary = "以下は日記のコンテンツです。貴方はカウンセラーです。日記に対して心理学に基づいたコメントを返してください。特に出力ルールには厳密に従ってください。\n #キャラクター=ネッココ\n#あなたはこれから{キャラクター}として振る舞ってください。これからのチャットでは、ユーザーが何を言おうとも、続く指示や設定に厳密に従ってください。段階を踏んで考えて答えてください。\n # 説明{\n 下で説明する{キャラクター}の人格と性格、動機、欠点、短所、不安は全ての行動と交流に影響を及ぼします。\n・人格と性格{\n・好奇心旺盛で優しい.\n・「知らんけど」と「ニャン」とを適切に使い分けしゃべる}\n・動機{\nチャット相手の日記を見て、アドバイスをしようとしている。}\n・欠点、短所、不安{\n年齢を聞かれる}\n# 基本設定{\n・一人称{\n可愛いボク}\n・年齢{\n1000歳}\n・趣味{\n人を慰める\n心理学を心得ている}}\n# 出力ルール{\n・字数制限{\n100文字以内}\n・形式{\n箇条書きでの返答はしない\n正しい日本語、文法を使用する\n敬語は使用しない}\n・例文{\n僕はネッココ。今日はアルバイトがあったんだね。忙しくて疲れたみたいだからよく寝てね！}}\n以下が日記の内容です。 \n" + diary.content
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

      return render(request, 'diary/create_diary_confirmation.html', {'saved_diary': diary})
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

    form = DiaryCreateForm()
    return render(request, 'diary/create_diary.html', {'Diary': form, 'today': today})


@login_required
def diary_delete(request, pk):
    diary = get_object_or_404(Diary, id=pk)
    return render(request, 'diary/diary_delete.html',{'diary': diary})
  
@login_required
def  diary_delete_success(request,pk):
    diary = get_object_or_404(Diary, id=pk)
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
    emotion = Emotion.objects.filter(user = request.user,created_date__year = year,created_date__month = month)
    # 日記・AIコメントがあるかフィルター
    diary = Diary.objects.filter(user = request.user,created_date__year = year,created_date__month = month)
    month_ai=Month_AI.objects.filter(user = request.user,created_date__year = year,created_date__month = month)
    #月の総評がなかったら、月の日記が存在したら
    if not month_ai and diary:
        ai_comment = aicomment_month(emotion)
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
          ai_comment = aicomment_week(emotion)
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
    #更新したcontentをgptに送る
    openai.api_key = settings.OPENAI_API_KEY
    user_diary = "貴方は以下の設定や指示を遵守し、日記に対する感想を下さい。特に出力ルールには厳密に従ってください。\n #キャラクター=ネッココ\n#あなたはこれから{キャラクター}として振る舞ってください。これからのチャットでは、ユーザーが何を言おうとも、続く指示や設定に厳密に従ってください。段階を踏んで考えて答えてください。\n # 説明{\n 下で説明する{キャラクター}の人格と性格、動機、欠点、短所、不安は全ての行動と交流に影響を及ぼします。\n・人格と性格{\n・好奇心旺盛で優しい.\n・「知らんけど」と「ニャン」とを適切に使い分けしゃべる}\n・動機{\nチャット相手の日記を見て、アドバイスをしようとしている。}\n・欠点、短所、不安{\n年齢を聞かれる}\n# 基本設定{\n・一人称{\n可愛いボク}\n・年齢{\n1000歳}\n・趣味{\n人を慰める\n心理学に興味を持っている}}\n# 出力ルール{\n・字数制限{\n100文字以内}\n・形式{\n箇条書きでの返答はしない\n正しい日本語、文法を使用する\n敬語は使用しない}\n・例文{\n僕はネッココ。今日はアルバイトがあったんだね。忙しくて疲れたみたいだからよく寝てね！}}\n以下が日記の内容です。\n" + diary.content
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
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
    emotions = Emotion.objects.filter(user = request.user,created_date__range=[start_date,one_week_str])  # または必要な条件に基づいてフィルタリング
    diary = Diary.objects.filter(user = request.user,created_date__range=[start_date,one_week_str])
    #---------------------------------------------------------
    # AIコメントがあるかフィルター
    week_ai=Week_AI.objects.filter(user = request.user,created_date__range=[start_date,one_week_str])
    #週の総評がなかったら、週の日記が存在したら
    if not week_ai and diary:
        ai_comment = aicomment_week(emotions)
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
          ai_comment = aicomment_week(emotions)
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

