from django.contrib.auth import login, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator

from .forms import RegisterForm, LoginForm

from .models import User


USERS_PER_PAGE = 12

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
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


def logout_view(request):
    logout(request)
    return redirect("projects:list")

def user_detail_view(request, user_id):
    user_obj = get_object_or_404(
        User.objects.prefetch_related("owned_projects"),
        id=user_id,
    )

    return render(
        request,
        "users/user-details.html",
        {"user": user_obj},
    )

def users_list_view(request):
    queryset = User.objects.order_by("-id")

    paginator = Paginator(queryset, USERS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "users/participants.html",
        {"participants": page_obj},
    )