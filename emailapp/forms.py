from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class SignUpForm(forms.Form):
    full_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"placeholder": "Your full name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "you@example.com"}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"placeholder": "Phone number"}))
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={"placeholder": "At least 8 characters"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Re-enter password"}))

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") and cleaned.get("confirm_password"):
            if cleaned["password"] != cleaned["confirm_password"]:
                self.add_error("confirm_password", "Passwords do not match.")
        return cleaned


class ComposeForm(forms.Form):
    tone = forms.ChoiceField(
        choices=[("formal", "Formal"), ("informal", "Informal")],
        widget=forms.Select()
    )
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"placeholder": "e.g. Meeting follow-up"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 6, "placeholder": "Write your email message here..."}))
    recipients = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 6, "placeholder": "One recipient per line: Full Name, email@example.com"}),
        help_text="Add up to 10 recipients, one per line, in this format: Full Name, email@example.com"
    )

    def clean_recipients(self):
        raw = self.cleaned_data["recipients"].strip()
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        if not lines:
            raise ValidationError("Add at least one recipient.")
        if len(lines) > 10:
            raise ValidationError("You can send to a maximum of 10 recipients per batch.")
        parsed = []
        seen = set()
        for number, line in enumerate(lines, start=1):
            parts = [part.strip() for part in line.split(",", 1)]
            if len(parts) != 2 or not parts[0] or not parts[1]:
                raise ValidationError(f"Line {number}: use Full Name, email@example.com")
            try:
                validate_email(parts[1])
            except ValidationError:
                raise ValidationError(f"Line {number}: enter a valid email address.")
            if parts[1].lower() in seen:
                raise ValidationError(f"Duplicate recipient email on line {number}.")
            seen.add(parts[1].lower())
            parsed.append((parts[0], parts[1]))
        return parsed
