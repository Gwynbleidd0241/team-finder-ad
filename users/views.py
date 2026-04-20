from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, ProfileEditForm, RegisterForm, UserPasswordChangeForm
from .models import User

USERS_PER_PAGE = 12


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            registered_user = form.save()
            login(request, registered_user)
            return redirect("projects:list")
    else:
        form = RegisterForm()

    return render(
        request,
        "users/register.html",
        {"form": form},
    )


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("projects:list")
    else:
        form = LoginForm()

    return render(
        request,
        "users/login.html",
        {"form": form},
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect("projects:list")


def users_list_view(request):
    users_qs = User.objects.order_by("-id")
    paginator = Paginator(users_qs, USERS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "users/participants.html",
        {"participants": page_obj},
    )


def user_detail_view(request, user_id):
    profile_user = get_object_or_404(
        User.objects.prefetch_related("owned_projects"),
        id=user_id,
    )

    return render(
        request,
        "users/user-details.html",
        {"user": profile_user},
    )


@login_required
def edit_profile_view(request):
    current_user = request.user

    if request.method == "POST":
        form = ProfileEditForm(
            request.POST,
            request.FILES,
            instance=current_user,
        )
        if form.is_valid():
            form.save()
            return redirect("users:detail", user_id=current_user.id)
    else:
        form = ProfileEditForm(instance=current_user)

    return render(
        request,
        "users/edit_profile.html",
        {"form": form},
    )


@login_required
def change_password_view(request):
    current_user = request.user

    if request.method == "POST":
        form = UserPasswordChangeForm(current_user, request.POST)
        if form.is_valid():
            updated_user = form.save()
            update_session_auth_hash(request, updated_user)
            return redirect("users:detail", user_id=current_user.id)
    else:
        form = UserPasswordChangeForm(current_user)

    return render(
        request,
        "users/change_password.html",
        {"form": form},
    )
