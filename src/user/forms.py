from django import forms
from allauth.socialaccount.forms import SignupForm

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages = {
            'unique': '既に同じメールアドレスが登録済みです。別のメールアドレスを登録お願いします。',
        }
        self.fields['password1'].error_messages = {
            'password_mismatch': 'パスワードが一致しません。',
        }
