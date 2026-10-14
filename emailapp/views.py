from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.utils.html import strip_tags

from .forms import SignUpForm, ComposeForm
from .models import UserProfile, EmailRecord


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "emailapp/home.html")


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        full_name = form.cleaned_data["full_name"].strip()
        email = form.cleaned_data["email"]
        user = User.objects.create_user(
            username=email,
            email=email,
            password=form.cleaned_data["password"],
            first_name=full_name,
        )
        UserProfile.objects.create(user=user, phone=form.cleaned_data["phone"])
        login(request, user)
        messages.success(request, "Your account is ready. Welcome to MailFlow!")
        return redirect("dashboard")
    return render(request, "emailapp/signup.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "emailapp/login.html"
    redirect_authenticated_user = True


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("home")


@login_required
def dashboard(request):
    records = EmailRecord.objects.filter(user=request.user)
    context = {
        "total_count": records.count(),
        "sent_count": records.filter(status="sent").count(),
        "failed_count": records.filter(status="failed").count(),
        "recent_records": records[:5],
    }
    return render(request, "emailapp/dashboard.html", context)


@login_required
def compose_email(request):
    form = ComposeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        tone = form.cleaned_data["tone"]
        subject = form.cleaned_data["subject"].strip()
        message_body = form.cleaned_data["message"].strip()
        results = []
        sender_name = request.user.get_full_name() or request.user.username
        for recipient_name, recipient_email in form.cleaned_data["recipients"]:
            personalized_body = f"Hi {recipient_name},\n\n{message_body}\n\nRegards,\n{sender_name}"
            try:
                email = EmailMessage(
                    subject=subject,
                    body=personalized_body,
                    from_email=None,
                    to=[recipient_email],
                    headers={"X-Mail-Tone": tone},
                )
                email.send(fail_silently=False)
                status = "sent"
                results.append((recipient_email, "Sent"))
            except Exception:
                status = "failed"
                results.append((recipient_email, "Failed"))
            EmailRecord.objects.create(
                user=request.user,
                recipient_name=recipient_name,
                recipient_email=recipient_email,
                subject=subject,
                message=personalized_body,
                tone=tone,
                status=status,
            )
        request.session["last_send_results"] = results
        messages.success(request, f"Processed {len(results)} email(s). Check each status below.")
        return redirect("history")
    return render(request, "emailapp/compose.html", {"form": form})


@login_required
def email_history(request):
    results = request.session.pop("last_send_results", [])
    records = EmailRecord.objects.filter(user=request.user)
    return render(request, "emailapp/history.html", {"records": records, "results": results})
