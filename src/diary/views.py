from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .models import Diary, Emotion
from user.models import CustomUser
from django.contrib.auth.decorators import login_required
from .forms import DiaryCreateForm
from django.shortcuts import get_object_or_404
from datetime import datetime, date
from django.views.generic.edit import UpdateView
from django.conf import settings
import openai
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
def positive_conversion(request, pk):
    diary = get_object_or_404(Diary, id=pk)
    openai.api_key = settings.OPENAI_API_KEY
    save_content = ""

    if 'save_button' in request.POST:
    # データベースへの保存
        diary.content = save_content
        diary.save()  # データベースの保存は最後に行う
        return redirect('diary:today_diary_detail', pk=pk)
    else:
        user_diary = "以下は日記のコンテンツです。ポジティブで前向きになれるよう、ネガティブな言葉を変換し、書き換えてください。あなたのセリフはいりません。\n" + diary.content
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_diary}
            ]
        )
        ai_content = response["choices"][0]["message"]["content"]
        save_content = ai_content


    return render(request, 'diary/positive_conversion.html', {'diary': diary, 'save_content':save_content })

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

