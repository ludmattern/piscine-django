from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
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


@login_required
@require_POST
def vote(request, tip_id, vote_type):
    tip = get_object_or_404(Tip, id=tip_id)
    user = request.user

    if vote_type == "up":
        if tip.upvotes.filter(id=user.id).exists():
            tip.upvotes.remove(user)
        else:
            tip.upvotes.add(user)
            tip.downvotes.remove(user)
    elif vote_type == "down":
        if tip.downvotes.filter(id=user.id).exists():
            tip.downvotes.remove(user)
        else:
            tip.downvotes.add(user)
            tip.upvotes.remove(user)

    return redirect("index")


@login_required
@require_POST
def delete_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    if request.user == tip.author or request.user.has_perm("ex.delete_tip"):
        tip.delete()
    return redirect("index")


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
