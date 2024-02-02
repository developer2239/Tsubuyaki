from django.shortcuts import render

# ログイン画面表示
def login(request):
    return render(request,"login.html")

# 新規アカウント作成画面
def signup(request):
    return render(request,"signup.html")