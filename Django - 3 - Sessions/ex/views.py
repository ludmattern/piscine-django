from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from .forms import TipForm, RegistrationForm, LoginForm
from .models import Tip

User = get_user_model()


def index(request):
    tips = Tip.objects.all().order_by("-date")
    form = TipForm()

    if request.method == "POST" and request.user.is_authenticated:
        form = TipForm(request.POST)
        if form.is_valid():
            tip = form.save(commit=False)
            tip.author = request.user
            tip.save()
            return redirect("index")

    return render(request, "ex/index.html", {"tips": tips, "form": form})


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

    return render(request, "ex/register.html", {"form": form})


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

    return render(request, "ex/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("index")
