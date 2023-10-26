from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):

    class Meta:
        model = CustomUser#ここでmodelを指定してモデル情報と紐づける
        fields = ["username", "password","email"]#扱うフィールド名を指定する