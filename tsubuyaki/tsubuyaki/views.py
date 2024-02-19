from hashlib import sha256
import json
from django.db import Error, IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from tsubuyaki.models.account import Account
from tsubuyaki.models.favorite import Favorite
from tsubuyaki.models.follow import Follow
from tsubuyaki.models.post import ExtendedJsonEncoder, Post


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
        "posts" : posts,
    }
    return render(request, "posts.html", params)

# つぶやき情報を返す
def fetch_posts(request):
    json_data = json.loads(str(request.body, encoding='utf-8'))
    post_id = json_data.get("post_id")
    post_list = []
    try:
        if post_id is None:
            posts = Post.objects.all().select_related("account").order_by("-created_at")[:20]
        else:
            posts = Post.objects.filter(post_id__lt = post_id).select_related("account").order_by("-created_at")[:20]
        
        isErrorHappened = False
    except Error:
        isErrorHappened = True
    params = {
        'is_error_happened' : isErrorHappened,
        'posts' : json.dumps(posts, cls=ExtendedJsonEncoder, ensure_ascii=False),
    }
    return JsonResponse(params)
    

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
        account = updated
    else:
        showed_account = Account.objects.get(account_id = account_id)
        account_id = showed_account.account_id
        account = showed_account

    # フォロー情報をフェッチ
    following = Follow.objects.filter(account_id = account_id).count()
    followed = Follow.objects.filter(follow_account_id = account_id).count()
    # 既にフォローしているか否か
    is_follow = True if Follow.objects.filter(account_id = updated.account_id,follow_account_id = account_id) else False

    # ユーザが投稿した呟きのみをフィルタリングする
    posts = Post.objects.filter(account_id = account_id).order_by("-created_at")
    params = {
        "posts" : posts,
        "account" :  account,
        "following" : following,
        "followed" : followed,
        "is_follow" : is_follow,
    }
    return render(request,"profile.html",params)

# つぶやき追加
def post(request):
    if request.method == "POST":
        content = request.POST.get("content")
        account = request.session["account"]
        account_id = account.account_id
        Post.objects.create(content = content, account_id = account_id)
        return redirect("/profile/")
    
# つぶやき削除
def delete(request):
    json_data = json.loads(str(request.body, encoding='utf-8'))
    # レコードの削除
    try:
        post = Post.objects.get(post_id = json_data.get("post_id"))
        post.delete()
        is_deleted = True
    except Error:
        is_deleted = False
        
    params = {
        'is_deleted' : is_deleted,
    }
    return JsonResponse(params)

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

# フォロー
def follow(request):
    target_account_id = request.GET.get("account_id")
    account_id = request.session["account"].account_id
    Follow.objects.create(account_id = account_id,follow_account_id = target_account_id)
    return redirect("/profile/?account_id="+ target_account_id)

# アンフォロー
def unfollow(request):
    target_account_id = request.GET.get("account_id")
    account_id = request.session["account"].account_id
    # レコードの削除
    follow = Follow.objects.filter(account_id = account_id,follow_account_id = target_account_id).delete()
    return redirect("/profile/?account_id="+ target_account_id)

# いいね追加・削除
def favorite(request):
    account_id = request.session["account"].account_id
    json_data = json.loads(str(request.body, encoding='utf-8'))
    post_id = json_data.get("post_id")
    try:
        # いいねが登録されてばレコードを削除、なければ登録
        favorite = Favorite.objects.filter(post_id = post_id, account_id = account_id).count()
        if favorite > 0:
            # ここでエラー
            print(favorite)
            target = Favorite.objects.filter(post_id = post_id, account_id = account_id).delete()
        else:
            Favorite.objects.create(post_id = post_id,account_id = account_id)
        isErrorHappened = False
    except Error as e:
        print(e)
        isErrorHappened = True
    params = {
        'is_error_happened' : isErrorHappened,
    }
    return JsonResponse(params)

# アカウントの削除
def dump_account(request):
    account_id = request.session["account"].account_id
    res = Account.objects.filter(account_id = account_id).delete()
    print(res)
    return redirect("/login/")