from functools import wraps

from django.shortcuts import redirect, render

from .content import ABOUT_SECTIONS, BLOG_POSTS, CONTACT_CHANNELS, FAQS, GAMES


def login_required_view(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("is_logged_in"):
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return wrapper


@login_required_view
def home(request):
    context = {
        "featured_games": GAMES[:8],
        "spotlight_game": GAMES[8],
        "trending_games": GAMES[9:15],
        "latest_posts": BLOG_POSTS[:4],
    }
    return render(request, "home.html", context)


@login_required_view
def aboutus(request):
    context = {
        "games": GAMES,
        "about_sections": ABOUT_SECTIONS,
    }
    return render(request, "aboutus.html", context)


@login_required_view
def gallery(request):
    return render(request, "gallery.html", {"games": GAMES})


@login_required_view
def blog(request):
    context = {
        "posts": BLOG_POSTS,
        "featured_post": BLOG_POSTS[4],
        "featured_game": GAMES[10],
    }
    return render(request, "blog.html", context)


@login_required_view
def contactus(request):
    context = {
        "contact_channels": CONTACT_CHANNELS,
        "faqs": FAQS,
        "hero_game": GAMES[1],
    }
    return render(request, "contactus.html", context)


def login_view(request):
    error_message = ""

    if request.session.get("is_logged_in"):
        return redirect("home")

    if request.method == "POST":
        user_id = request.POST.get("userid", "").strip()
        password = request.POST.get("password", "").strip()

        if user_id == "aman" and password == "123":
            request.session["is_logged_in"] = True
            request.session["userid"] = "aman"
            return redirect("home")
        else:
            error_message = "Invalid credentials. Only the specified userid and password are valid."

    return render(
        request,
        "login.html",
        {
            "error_message": error_message,
        },
    )


def logout_view(request):
    request.session.flush()
    return redirect("login")
