from hashlib import sha256
from django.db import IntegrityError
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
        
# ログアウト
def logout(request):
    # セッション破棄
    request.session.clear() 
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
        try:
            Account.objects.create(name = name, id = id, password = hashed_password)
        except IntegrityError:
            errmsg = str(id) + "は既に使用されています。他のIDを選択してください。"
            return redirect("/signup/?errmsg=" + errmsg)
            
        return redirect("/login/")


# つぶやき・ポスト一覧画面
def posts(request):
    posts = Post.objects.all().order_by("-created_at") 
    params = {
        "posts" : posts
    }
    return render(request, "posts.html", params)

# プロフィール画面
def profile(request):

    # セッションのアカウント情報を更新する
    my_account = request.session["account"]
    updated = Account.objects.get(id = my_account.id)
    request.session["account"] = updated

    # ユーザIDパラメータの取得
    account_id = request.GET.get("account_id")
    if  account_id is None:
        account_id = my_account.account_id
        account = my_account
    else:
        showed_account = Account.objects.get(account_id = account_id)
        account_id = showed_account.account_id
        account = showed_account

    # ユーザが投稿した呟きのみをフィルタリングする
    posts = Post.objects.filter(account_id = account_id).order_by("created_at")
    params = {
        "posts" : posts,
        "account" :  account
    }
    return render(request,"profile.html",params)

# つぶやき追加
def post(request):
    if request.method == "POST":
        content = request.POST.get("content")
        account = request.session["account"]
        account_id = account.account_id
        Post.objects.create(content = content, account_id = account_id)
        return redirect("/posts/")
    
# つぶやき削除
def delete(request):
    post_id = request.GET.get("post_id")
    # レコードの削除
    post = Post.objects.get(post_id = post_id)
    post.delete()
    return redirect("/profile/")

# アカウントカスタム画面
def custom(request):
    return render(request,"custom.html")

# プロフィール文の変更
def editProfile(request):
    if request.method == "POST":
        # 変更した情報をDBへ
        account = request.session["account"]
        my_account = Account.objects.get(account_id = account.account_id)
        profile = request.POST.get("profile")
        my_account.profile = profile
        my_account.save()
        return redirect("/profile/")
