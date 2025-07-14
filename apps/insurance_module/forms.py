from django import forms
from apps.account_module.models import SubUser
from django.core import validators
from jalali_date.fields import JalaliDateField
from apps.home_module.models import PilgrimageDestination
from apps.account_module.models import SubUser
from jalali_date.widgets import AdminJalaliDateWidget
from datetime import date, timedelta, datetime
import jdatetime
from iranian_cities.models import Province, County
from django.db.models import Q


class CreateInsuranceForm(forms.Form):

    destination = forms.ModelChoiceField(
        queryset=PilgrimageDestination.objects.all(),
        empty_label="مقصد را انتخاب کنید",
        label="مقاصد زیارتی",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    # subsets = forms.ModelMultipleChoiceField(
    #     queryset=SubUser.objects.none(),
    #     label="زائران خود را انتخاب کنید",
    #     required=False,
    #     widget=forms.widgets.SelectMultiple(
    #         attrs={"id": "product-select", "class": "form-control"}
    #     ),
    # )

    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        empty_label="استان را انتخاب کنید",
        label="استان مبدا",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    county = forms.ModelChoiceField(
        queryset=County.objects.all(),
        empty_label="شهر را انتخاب کنید",
        label="شهر مبدا",
        required=False,
    )

    insurance_maneger = forms.BooleanField(
        label="مدیر گروه بیمه شود",
        required=False,
        # widget=forms.widgets.RadioSelect(attrs={"class": "form-radio-input"}),
    )

    start_date = forms.CharField(widget=AdminJalaliDateWidget(attrs={"readonly": True}))

    end_date = forms.CharField(
        widget=AdminJalaliDateWidget(attrs={"class": "d-none", "readonly": True})
    )

    def clean_start_date(self):
        get_start_date = self.cleaned_data["start_date"].split("/")

        start_date = jdatetime.JalaliToGregorian(
            int(get_start_date[0]), int(get_start_date[1]), int(get_start_date[2])
        )

        start_date = date(start_date.gyear, start_date.gmonth, start_date.gday)

        today = date.today()

        if start_date <= today:
            forms.ValidationError("تاریخ شروع بیمه باید از فردای روز جاری انتخاب شود")
        else:
            return start_date

    def clean_end_date(self):

        get_start_date = self.cleaned_data["start_date"]

        get_end_date = self.cleaned_data["end_date"].split("/")

        end_date = jdatetime.JalaliToGregorian(
            int(get_end_date[0]), int(get_end_date[1]), int(get_end_date[2])
        )

        end_date = date(end_date.gyear, end_date.gmonth, end_date.gday)

        max_day = get_start_date + timedelta(days=15)

        if end_date > max_day:
            forms.ValidationError("نهایت مدت بیمه 15 روز است")
        else:
            return end_date


class CreateSubUserForm(forms.Form):
    full_name = forms.CharField(
        max_length=255,
        help_text="نام و نام خانوادگی  را وارد کنید",
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


class UpdateSubUserModelForm(forms.ModelForm):
    class Meta:
        model = SubUser
        exclude = ["manager"]

        validators = {
            "national_code": validators.RegexValidator(
                r"^[0-9]{10}$", message="فرمت کد ملی صحیح نمی باشد"
            )
        }

        widgets = {
            "full_name": forms.widgets.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "نام و نام خانوادگی  را وارد کنید",
                }
            ),
            "national_code": forms.widgets.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "کدملی خود را وارد کنید",
                }
            ),
        }


class SearchSubsForm(forms.Form):

    full_name = forms.CharField(
        max_length=220,
        label="نام و نام خانوادگی",
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "نام و نام خانوادگی  را وارد کنید",
            }
        ),
    )

    national_code = forms.CharField(
        max_length=120,
        label="کدملی",
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "کدملی خود را وارد کنید",
            }
        ),
    )
