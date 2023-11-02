from django import forms
from .models import Diary

class DiaryCreateForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['content', 'photo1', 'photo2', 'photo3', 'photo4', 'movie1', 'movie2', 'movie3', 'movie4']
