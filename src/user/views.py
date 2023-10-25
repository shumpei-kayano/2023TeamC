from django.shortcuts import render

def signup(request):
    return render(request, 'user/signup.html')
def signup_email(request):
    return render(request, 'user/signup_email.html')
def check_email(request):
    return render(request, 'user/check_email.html')