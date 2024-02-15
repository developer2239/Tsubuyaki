"""
URL configuration for tsubuyaki project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import tsubuyaki.views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    # ログイン
    path('',v.login),
    path('login/',v.login),
    # ログアウト
    path('logout/',v.logout),
    # サインアップ
    path('signup/',v.signup),
    # ポスト・つぶやき一覧画面
    path('posts/',v.posts),
    # プロフィール画面
    path('profile/',v.profile),
    # アカウントカスタム画面
    path('custom/',v.custom),

    # つぶやき追加ボタン、サブミット
    path('post/',v.post),
    # つぶやき×ボタン、つぶやき削除
    path('delete/',v.delete),

    # プロフィール変更
    path('profile/edit/',v.editProfile),

    # フォロー
    path('follow/',v.follow),
    # アンフォロー
    path('unfollow/',v.unfollow),

    # いいね追加
    path('favorite/',v.favorite),

]
