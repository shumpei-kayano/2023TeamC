from django import forms
from .models import Diary

class DiaryCreateForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['content', 'photo1', 'photo2', 'photo3', 'photo4', 'movie1', 'movie2', 'movie3', 'movie4',]
        
        widgets = {
                    'content': forms.Textarea(attrs={'class': 'content__textarea', 'placeholder': 'ここに書いてください（最大1000文字）', 'oninput': 'countCharacters(this)'}),
                    'photo1': forms.ClearableFileInput(attrs={'class': 'content__photo-btn', 'type': 'button'}),
                    'photo2': forms.ClearableFileInput(attrs={'class': 'content__photo-btn', 'type': 'button'}),
                    'photo3': forms.ClearableFileInput(attrs={'class': 'content__photo-btn', 'type': 'button'}),
                    'photo4': forms.ClearableFileInput(attrs={'class': 'content__photo-btn', 'type': 'button'}),
                    'movie1': forms.TextInput(attrs={'class': 'content__movie-btn', 'type': 'button'}),
                    'movie2': forms.TextInput(attrs={'class': 'content__movie-btn', 'type': 'button'}),
                    'movie3': forms.TextInput(attrs={'class': 'content__movie-btn', 'type': 'button'}),
                    'movie4': forms.TextInput(attrs={'class': 'content__movie-btn', 'type': 'button'}),
                }