from django import forms
from .models import Diary

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model


class DiaryCreateForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['content', 'photo1', 'photo2', 'photo3', 'photo4', 'movie1', 'movie2', 'movie3', 'movie4',]
        
        widgets = {
                    # テキストエリアとボタンを動的に表示するための属性を追加
                    'content': forms.Textarea(attrs={'class': 'content__textarea', 'placeholder': 'ここに書いてください（最大1000文字）', 'oninput': 'countCharacters(this)'}),
                    'photo1': forms.FileInput(attrs={'onchange': 'updateFileName(this, "file_name_photo1")'}),
                    'photo2': forms.FileInput(attrs={'onchange': 'updateFileName(this, "file_name_photo2")'}),
                    'photo3': forms.FileInput(attrs={'onchange': 'updateFileName(this, "file_name_photo3")'}),
                    'photo4': forms.FileInput(attrs={'onchange': 'updateFileName(this, "file_name_photo4")'}),
                    'movie1': forms.FileInput(attrs={'onchange': 'updateFileName(this, "file_name_movie1")'}),
                    'movie2': forms.FileInput(attrs={'onchange': 'updateFileName(this, "file_name_movie2")'}),
                    'movie3': forms.FileInput(attrs={'onchange': 'updateFileName(this, "file_name_movie3")'}),
                    'movie4': forms.FileInput(attrs={'onchange': 'updateFileName(this, "file_name_movie4")'}),
                }

                    # 'photo1': forms.ClearableFileInput(attrs={'class': 'content__photo-btn', 'type': 'button'}),
                    # 'photo2': forms.ClearableFileInput(attrs={'class': 'content__photo-btn', 'type': 'button'}),
                    # 'photo3': forms.ClearableFileInput(attrs={'class': 'content__photo-btn', 'type': 'button'}),
                    # 'photo4': forms.ClearableFileInput(attrs={'class': 'content__photo-btn', 'type': 'button'}),
                    # 'movie1': forms.TextInput(attrs={'class': 'content__movie-btn', 'type': 'button'}),
                    # 'movie2': forms.TextInput(attrs={'class': 'content__movie-btn', 'type': 'button'}),
                    # 'movie3': forms.TextInput(attrs={'class': 'content__movie-btn', 'type': 'button'}),
                    # 'movie4': forms.TextInput(attrs={'class': 'content__movie-btn', 'type': 'button'}),
                    
class CustomUserChangeFormBase(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username']  # ユーザーの編集可能なフィールドを指定
        labels = {
        'username': 'ユーザーネーム',
    }
class CustomUserChangeForm(CustomUserChangeFormBase):
  pass
class ImageDeleteForm(forms.Form):
    photo1_delete = forms.BooleanField(required=False)
    photo2_delete = forms.BooleanField(required=False)
    photo3_delete = forms.BooleanField(required=False)
    photo4_delete = forms.BooleanField(required=False)
    movie1_delete = forms.BooleanField(required=False)
    movie2_delete = forms.BooleanField(required=False)
    movie3_delete = forms.BooleanField(required=False)
    movie4_delete = forms.BooleanField(required=False)
