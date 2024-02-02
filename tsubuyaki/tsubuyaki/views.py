from django.shortcuts import render
from django.shortcuts import redirect

# ログイン画面表示
def login(request):
    if request.method == "GET":
        return render(request,"login.html")
    if request.method == "POST":
        return redirect("/posts/")

# 新規アカウント作成画面
def signup(request):
    return render(request,"signup.html")

# つぶやき・ポスト一覧画面
def posts(request):
    return render(request,"posts.html")

# プロフィール画面
def profile(request):
    return render(request,"profile.html")