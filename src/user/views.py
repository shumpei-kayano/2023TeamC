from django.shortcuts import render
from django.views.generic.edit import FormView
# from .forms import CustomUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from allauth.account.views import SignupView
from .forms import CustomSignupForm
from django import forms

def account_top(request):
    return render(request, 'account_top.html')

def tutorial1(request):
    return render(request, 'tutorial1.html')

def logout(request):
    return render(request, 'logout.html')
class CustomSignupView(SignupView):
    form_class = CustomSignupForm

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

    def form_valid(self, form):
        try:
            form.validate_unique_email(form.cleaned_data['email'])
        except forms.ValidationError as e:
            # 一意でない場合、エラーメッセージをフォームに追加してページを再描画
            form.add_error('email', e)
            return self.form_invalid(form)

        # メールアドレスが一意であれば通常のフォーム処理を継続
        return super().form_valid(form)

def email(request):
    return render(request, 'email.html')

def password_reset(request):
    return render(request, 'password_reset.html')
