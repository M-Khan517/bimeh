from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from apps.account_module.models import User


class RegisterForm(forms.Form):
    full_name = forms.CharField(
        max_length=255,
        help_text="نام و نام خانوادگی خود را وارد کنید",
        label="نام و نام خانوادگی",
        widget=forms.widgets.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "نام و نام خانوادگی خود را وارد کنید",
            }
        ),
    )

    national_code = forms.CharField(
        max_length=120,
        help_text="کد ملی خود را وارد کنید",
        label="کد ملی",
        validators=[
            validators.RegexValidator(
                r"^[0-9]{10}$", message="فرمت کد ملی صحیح نمی باشد"
            )
        ],
        widget=forms.widgets.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "کدملی خود را وارد کنید",
            }
        ),
    )

    # email = forms.CharField(
    #     max_length=120,
    #     help_text="ایمیل خود را واردکنید",
    #     label="ایمیل",
    #     widget=forms.widgets.EmailInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "ایمیل خود را وارد کنید",
    #         }
    #     ),
    # )

    phone = forms.CharField(
        max_length=120,
        help_text=" شماره تلفن خود را وارد کنید",
        label="شماره تلفن",
        validators=[
            validators.RegexValidator(
                r"^((\+98|0)9\d{9})$", message="شماره تلفن صحیح نمیباشد"
            )
        ],
        widget=forms.widgets.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "شماره تلفن خود را وارد کنید",
            }
        ),
    )

    password = forms.CharField(
        max_length=32,
        help_text="رمز عبور خود را وارد کنید",
        label="رمز عبور",
        widget=forms.widgets.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "رمز خود را وارد کنید",
                "aria-describedby": "password",
            }
        ),
    )

    confirm_password = forms.CharField(
        max_length=32,
        help_text="تکرار رمز عبور خود را وارد کنید",
        label="تکرار رمز عبور",
        widget=forms.widgets.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "تکرار رمز خود را وارد کنید",
            }
        ),
    )

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get("confirm_password")
        password = self.cleaned_data.get("password")

        if confirm_password != password:
            raise forms.ValidationError("رمز عبور و تکرار آن مغایرت دارند.")

        return confirm_password


class LoginForm(forms.Form):

    phone = forms.CharField(
        max_length=120,
        help_text=" شماره تلفن خود را وارد کنید",
        label="شماره تلفن",
        validators=[
            validators.RegexValidator(
                r"^((\+98|0)9\d{9})$", message="شماره تلفن صحیح نمیباشد"
            )
        ],
        widget=forms.widgets.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "شماره تلفن خود را وارد کنید",
                "autofocus": "",
            }
        ),
    )

    # password = forms.CharField(
    #     max_length=32,
    #     help_text="رمز عبور خود را وارد کنید",
    #     label="رمز عبور",
    #     widget=forms.widgets.PasswordInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "رمز خود را وارد کنید",
    #             "aria-describedby": "password",
    #         }
    #     ),
    # )

    remember_me = forms.BooleanField(
        required=False,
        label="مرا بخاطر بسپار",
        widget=forms.widgets.CheckboxInput(attrs={"class": "form-check-input"}),
    )


class VerifyAcountForm(forms.Form):
    num1 = forms.CharField(
        max_length=1,
        min_length=1,
        widget=forms.widgets.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control auth-input h-px-50 text-center numeral-mask mx-1 my-2",
                "maxlength": "1",
                "type": "tel",
                "onkeyup": "nextInput(this)",
            }
        ),
    )

    num2 = forms.CharField(
        max_length=1,
        min_length=1,
        widget=forms.widgets.TextInput(
            attrs={
                "class": "form-control auth-input h-px-50 text-center numeral-mask mx-1 my-2",
                "maxlength": "1",
                "type": "tel",
                "onkeyup": "nextInput(this)",
            }
        ),
    )

    num3 = forms.CharField(
        max_length=1,
        min_length=1,
        widget=forms.widgets.TextInput(
            attrs={
                "class": "form-control auth-input h-px-50 text-center numeral-mask mx-1 my-2",
                "maxlength": "1",
                "type": "tel",
                "onkeyup": "nextInput(this)",
            }
        ),
    )

    num4 = forms.CharField(
        max_length=1,
        min_length=1,
        widget=forms.widgets.TextInput(
            attrs={
                "class": "form-control auth-input h-px-50 text-center numeral-mask mx-1 my-2",
                "maxlength": "1",
                "type": "tel",
                "onkeyup": "nextInput(this)",
            }
        ),
    )

    num5 = forms.CharField(
        max_length=1,
        min_length=1,
        widget=forms.widgets.TextInput(
            attrs={
                "class": "form-control auth-input h-px-50 text-center numeral-mask mx-1 my-2",
                "maxlength": "1",
                "type": "tel",
                "onkeyup": "nextInput(this)",
            }
        ),
    )

    num6 = forms.CharField(
        max_length=1,
        min_length=1,
        widget=forms.widgets.TextInput(
            attrs={
                "class": "form-control auth-input h-px-50 text-center numeral-mask mx-1 my-2",
                "maxlength": "1",
                "type": "tel",
                "onkeyup": "nextInput(this)",
            }
        ),
    )


class ForgotPasswordForm(forms.Form):
    phone = forms.CharField(
        max_length=120,
        help_text=" شماره تلفن خود را وارد کنید",
        label="شماره تلفن",
        validators=[
            validators.RegexValidator(
                r"^((\+98|0)9\d{9})$", message="شماره تلفن صحیح نمیباشد"
            )
        ],
        widget=forms.widgets.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "شماره تلفن خود را وارد کنید",
                "autofocus": "",
            }
        ),
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        max_length=32,
        help_text="رمز عبور خود را وارد کنید",
        label="رمز عبور",
        widget=forms.widgets.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "رمز خود را وارد کنید",
                "aria-describedby": "password",
            }
        ),
    )

    confirm_password = forms.CharField(
        max_length=32,
        help_text="تکرار رمز عبور خود را وارد کنید",
        label="تکرار رمز عبور",
        widget=forms.widgets.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "تکرار رمز خود را وارد کنید",
            }
        ),
    )

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get("confirm_password")
        password = self.cleaned_data.get("password")

        if confirm_password != password:
            raise forms.ValidationError("رمز عبور و تکرار آن مغایرت دارند.")

        return confirm_password


class UpdateUserModelForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ["full_name", "national_code", "phone"]

        validators = {
            "phone": validators.RegexValidator(
                r"^((\+98|0)9\d{9})$", message="شماره تلفن صحیح نمیباشد"
            ),
            "national_code": validators.RegexValidator(
                r"^[0-9]{10}$", message="فرمت کد ملی صحیح نمی باشد"
            ),
        }

        widgets = {
            "phone": forms.widgets.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "شماره تلفن خود را وارد کنید",
                }
            ),
            "full_name": forms.widgets.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "نام و نام خانوادگی خود را وارد کنید",
                }
            ),
            "national_code": forms.widgets.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "کدملی خود را وارد کنید",
                }
            ),
        }
