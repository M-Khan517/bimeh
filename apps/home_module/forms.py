from django import forms
from .models import Contact
from django.core import validators


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = Contact

        exclude = ["created_at"]

        widgets = {
            "full_name": forms.widgets.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "نام و نام خانوادگی خود را وارد کنید",
                }
            ),
            "message": forms.widgets.Textarea(
                attrs={"class": "form-control", "rows": 8}
            ),
            "phone": forms.widgets.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "شماره تلفن خود را وارد کنید",
                }
            ),
        }
