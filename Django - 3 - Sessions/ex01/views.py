from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from .forms import RegistrationForm, LoginForm

User = get_user_model()


def index(request):
    return render(request, "ex01/index.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect("index")
    else:
        form = RegistrationForm()

    return render(request, "ex01/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("index")
    else:
        form = LoginForm()

    return render(request, "ex01/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("index")
