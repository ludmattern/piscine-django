from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from .models import Tip

User = get_user_model()


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, required=True, label="Confirm Password"
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match.")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Invalid username or password.")
            self.user = user
        return cleaned_data


class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Share your tip..."}
            ),
        }
