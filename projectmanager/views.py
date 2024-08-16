from django.shortcuts import render
from django.contrib.auth.models import User


def dashboard(request):
    return render(request, "../templates/projectmanager/base.html")


def user_list(request):

    users = User.objects.exclude(username=request.user.username)

    return render(
        request, "../templates/projectmanager/userlist.html", {"users": users}
    )
