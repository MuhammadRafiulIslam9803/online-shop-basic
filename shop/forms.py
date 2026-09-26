
# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm


# class CustomerRegistrationForm(UserCreationForm):
#     username = forms.CharField(
#         label="Username", widget=forms.TextInput(attrs={"class": "form-control"})
#     )
#     password1 = forms.CharField(
#         label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
#     )
#     password2 = forms.CharField(
#         label="Confirm Password",
#         widget=forms.PasswordInput(attrs={"class": "form-control"}),
#     )
#     email = forms.CharField(
#         required=True, widget=forms.EmailInput(attrs={"class": "form-control"})
#     )

#     class Meta:
#         model = User
#         fields = ["username", "email", "password1", "password2"]
#         labels = {"email": "Email"}
#         widgets = {"username": forms.TextInput(attrs={"class": "form-control"})}

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomerRegistrationForm(UserCreationForm):

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            "class": (
                "w-full px-4 py-3 border border-gray-300 rounded-lg "
                "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                "focus:border-indigo-500 transition"
            ),
            "placeholder": "Enter your username",
            "autocomplete": "username",
        })
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={
            "class": (
                "w-full px-4 py-3 border border-gray-300 rounded-lg "
                "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                "focus:border-indigo-500 transition"
            ),
            "placeholder": "Enter your email address",
            "autocomplete": "email",
        })
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": (
                "w-full px-4 py-3 border border-gray-300 rounded-lg "
                "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                "focus:border-indigo-500 transition"
            ),
            "placeholder": "Create a password",
            "autocomplete": "new-password",
        })
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": (
                "w-full px-4 py-3 border border-gray-300 rounded-lg "
                "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                "focus:border-indigo-500 transition"
            ),
            "placeholder": "Confirm your password",
            "autocomplete": "new-password",
        })
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

