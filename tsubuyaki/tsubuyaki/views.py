from hashlib import sha256
from django.shortcuts import render
from django.shortcuts import redirect
from tsubuyaki.models.account import Account

# ログイン画面表示
def login(request):
    if request.method == "GET":
        return render(request,"login.html")
    if request.method == "POST":
        return redirect("/posts/")

# 新規アカウント作成画面
def signup(request):
    if request.method == "GET":
        return render(request,"signup.html")
    elif request.method == "POST":
        # パラメータ取得
        name = request.POST.get("name")
        id = request.POST.get("id")
        password = request.POST.get("password")
        # パスワードのハッシュ化
        hashed_password = sha256(password.encode()).hexdigest()
        Account.objects.create(name = name, id = id, password = hashed_password)
        return redirect("/login")


# つぶやき・ポスト一覧画面
def posts(request):
    return render(request,"posts.html")

# プロフィール画面
def profile(request):
    return render(request,"profile.html")

# アカウントカスタム画面
def custom(request):
    return render(request,"delete.html")