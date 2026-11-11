from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .models import User
from .forms import RegisterForm, LoginForm, ProfileEditForm
from django.core.paginator import Paginator
# from django.contrib.auth import authenticate


def participants_view(request):
    """Страница со списком всех пользователей с пагинацией по 12 профилей"""
    participants_list = User.objects.all().order_by("id")

    paginator = Paginator(participants_list, 12)
    page_number = request.GET.get("page")
    participants = paginator.get_page(page_number)

    return render(request, "users/participants.html", {
        "participants": participants
    })


def user_detail_view(request, pk):
    """Публичная страница отдельного пользователя"""
    profile_user = get_object_or_404(User, pk=pk)
    return render(request, "users/user-details.html", {"user": profile_user})


def register_view(request):
    """Регистрация нового пользователя"""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    """Вход в систему"""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            return redirect("projects:project_list")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    """Выход из аккаунта"""
    logout(request)
    return redirect("projects:project_list")


@login_required
def edit_profile_view(request):
    """Редактирование профиля пользователя"""
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:user_detail", pk=request.user.pk)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def change_password_view(request):
    """Смена пароля для авторизованного пользователя"""
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("users:user_detail", pk=request.user.pk)
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "users/change_password.html", {"form": form})
