from hashlib import sha256
from django.shortcuts import render
from django.shortcuts import redirect
from tsubuyaki.models.account import Account
from tsubuyaki.models.post import Post

# ログイン画面表示
def login(request):
    if request.method == "GET":
        return render(request,"login.html")
    if request.method == "POST":
        # パラメータ取得
        id = request.POST.get("id")
        password = request.POST.get("password")
        # パスワードのハッシュ化
        hashed_password = sha256(password.encode()).hexdigest()
        # アカウント情報取得
        account = Account.objects.filter(id = id, password = hashed_password)
        if len(account) > 0:
            #セッションにログイン情報を格納
            request.session["account"] = account[0]
            return redirect("/posts/")
        else:
            return redirect("/login/")

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
        return redirect("/login/")


# つぶやき・ポスト一覧画面
def posts(request):
    posts = Post.objects.all()
    params = {
        "posts" : posts
    }
    return render(request, "posts.html", params)

# プロフィール画面
def profile(request):
    return render(request,"profile.html")

# つぶやき追加
def post(request):
    if request.method == "POST":
        content = request.POST.get("content")
        account = request.session["account"]
        account_id = account.account_id
        Post.objects.create(content = content, account_id = account_id)
        return redirect("/posts/")

# アカウントカスタム画面
def custom(request):
    return render(request,"delete.html")
