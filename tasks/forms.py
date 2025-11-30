# tasks/forms.py
from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Task

# Existing TaskForm (leave as-is)
class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )

    class Meta:
        model = Task
        fields = ["title", "description", "is_completed", "priority", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")
        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError("The date of entry cannot be in the past.")
        return due_date


# Add this SignUpForm for (bootstrap attrs)
class SignUpForm(UserCreationForm):
    """Bootstrap-styled Django signup form."""

    class Meta:
        model = User
        # include email so user can register with email
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        # call parent constructor
        super().__init__(*args, **kwargs)
        # iterate fields and set bootstrap classes & placeholder
        for name, field in self.fields.items():
            widget = field.widget
            widget_name = widget.__class__.__name__.lower()

            # default placeholder: field label
            placeholder = field.label if field.label else name.capitalize()

            if "checkbox" in widget_name:
                widget.attrs.update({"class": "form-check-input"})
            elif "select" in widget_name:
                widget.attrs.update({"class": "form-select", "placeholder": placeholder})
            else:
                # text inputs, password inputs, email, etc.
                widget.attrs.update({"class": "form-control", "placeholder": placeholder})


# LOGIN FORM (Bootstrap attrs)
class LoginForm(AuthenticationForm):
    """Bootstrap-styled Django login form."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            placeholder = field.label or name.capitalize()
            widget = field.widget
            widget_type = widget.__class__.__name__.lower()

            if "checkbox" in widget_type:
                widget.attrs.update({"class": "form-check-input"})
            else:
                widget.attrs.update({
                    "class": "form-control",
                    "placeholder": placeholder
                })