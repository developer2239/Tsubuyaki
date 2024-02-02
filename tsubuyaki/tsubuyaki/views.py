from django.shortcuts import render

# ログイン画面表示
def login(request):
    return render(request,"login.html")