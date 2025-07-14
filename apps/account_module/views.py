from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import datetime
from django.utils import timezone
from web_project import TemplateLayout
from .forms import (
    RegisterForm,
    LoginForm,
    VerifyAcountForm,
    ForgotPasswordForm,
    ResetPasswordForm,
    UpdateUserModelForm,
)
from utils.import_date.import_excel import import_data
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, JsonResponse
from utils.sender.send_sms import send, send_with_pattern
from .models import User, SubUser
from django.contrib import messages
from django.contrib.auth import login, logout


class RegisterView(View):
    def get(self, request):

        form = RegisterForm()

        context = {"form": form}

        return render(request, "account_module/register.html", context)

    def post(self, request):

        form = RegisterForm(request.POST)

        if form.is_valid():

            full_name = form.cleaned_data.get("full_name")

            national_code = form.cleaned_data.get("national_code")

            phone = form.cleaned_data.get("phone")
            username = phone
            password = form.cleaned_data.get("password")

            users = User.objects.all()

            check_phone = users.filter(phone=phone).exists()
            check_national_code = users.filter(national_code=national_code).exists()

            if check_national_code | check_phone:
                if check_phone:
                    form.add_error("phone", "شماره تلفن تکراری است")
                else:
                    form.add_error("national_code", "کدملی تکراری است")
            else:
                new_user = User(
                    full_name=full_name,
                    phone=phone,
                    national_code=national_code,
                    is_active=False,
                )

                new_user.set_password(password)

                new_user.save()

                request.session["user"] = {
                    "action": "active_account",
                    "phone": new_user.phone,
                }

                messages.success(request, "ثبت نام با موفقیت انجام شد")

                return redirect("login")

        # form = RegisterForm(request.POST)

        context = {"form": form}

        return render(request, "account_module/register.html", context)


class LoginView(View):
    def get(self, request):
        form = LoginForm()

        context = {"form": form}

        return render(request, "account_module/login.html", context)

    def post(self, request: HttpRequest):
        form = LoginForm(request.POST)

        if form.is_valid():

            phone = form.cleaned_data.get("phone")

            find_user = None
            try:
                find_user = User.objects.get(phone=phone)
            except:
                find_user = None

            if find_user:

                # ? generate new verify code
                find_user.save()

                # send(phone, find_user.verify_code)
                send_with_pattern(344666, phone, [find_user.verify_code])

                if request.session.get("user"):
                    del request.session["user"]
                request.session["user"] = {"phone": phone}

                return redirect("verify_account")

            else:
                form.add_error(
                    "phone",
                    "حساب یافت نشد . !",
                )

        context = {"form": form}
        return render(request, "account_module/login.html", context)


def logout_user(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
    return redirect("login")


class VerifyAccountView(View):
    def get(self, request):
        if request.session.get("user"):
            form = VerifyAcountForm()
            user_phone = request.session["user"]["phone"]
            user = get_object_or_404(User, phone=user_phone)

            context = {
                "form": form,
                "phone": user.phone,
                "phone_first": user.phone[:4],
                "phone_last": user.phone[7:],
                "expire": int(user.expire_verify_code.timestamp() * 1000),
            }

            return render(request, "account_module/verify_account.html", context)
        return redirect("register")

    def post(self, request):
        form = VerifyAcountForm(request.POST)

        if form.is_valid():
            code = "".join([form.cleaned_data.get(f"num{i}") for i in range(1, 7)])
            user_phone = request.session["user"]["phone"]
            user = get_object_or_404(User, phone=user_phone)

            if user.verify_code == code:
                user.is_active = True  # اگر لازمه
                user.save()
                del request.session["user"]

                login(request, user)
                request.session.modified = True  # سشن رو مطمئن ذخیره کن

                messages.success(request, "خوش آمدید.")
                return redirect("home")
            else:
                form.add_error("num1", "کد صحیح نمی‌باشد")

        return render(request, "account_module/verify_account.html", {"form": form})


class ForgotPasswordView(View):
    def get(self, request):

        form = ForgotPasswordForm()

        context = {"form": form}

        return render(request, "account_module/forgot_password.html", context)

    def post(self, request):

        form = ForgotPasswordForm(request.POST)

        if form.is_valid():

            phone = form.cleaned_data.get("phone")

            get_user = None

            try:
                get_user = User.objects.get(phone=phone)
            except:
                get_user = None

            if get_user:
                get_user.save()

                # send(get_user.phone, get_user.verify_code)
                send_with_pattern(344666, get_user.phone, [get_user.verify_code])

                request.session["user"] = {
                    "phone": get_user.phone,
                    "action": "forgot_password",
                }

                messages.success(request, "کد ارسال شد ")

                return render(request, "account_module/forgot_password.html")
            else:
                form.add_error("phone", "حساب یافت نشد.")

        context = {"form": form}
        return render(request, "account_module/forgot_password.html", context)


class ResetPassowrdView(View):
    def get(self, request: HttpRequest):

        if (
            request.session["user"]["action"] == "forgot_password"
            and request.session["user"]["verifyed"] == True
        ):

            form = ResetPasswordForm()

            user_phone = request.session["user"]["phone"]

            user_phone_display_first = user_phone[:4]

            user_phone_display_last = user_phone[7:]

            context = {
                "form": form,
                "phone_first": user_phone_display_first,
                "phone_last": user_phone_display_last,
            }

            return render(request, "account_module/reset_password.html", context)

        return HttpResponseNotFound()

    def post(self, request):

        form = ResetPasswordForm(request.POST)

        phone = request.session["user"]["phone"]

        if form.is_valid():

            get_user = get_object_or_404(User, phone=phone)

            new_password = form.cleaned_data.get("password")

            get_user.set_password(new_password)

            get_user.save()

            del request.session["user"]

            messages.success(request, "رمز شما با موفقیت تغییر کرد")

            return render(request, "account_module/reset_password.html")

        context = {"form": form}

        return render(request, "account_module/reset_password.html", context)


class UpdateUserView(LoginRequiredMixin, TemplateView):
    template_name = "account_module/update_user.html"

    def get_context_data(self, **kwargs):

        get_user = self.request.user

        form = UpdateUserModelForm(instance=get_user)

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        if not "form" in context:
            context["form"] = form

        return context

    def post(self, request, *args, **kwargs):
        get_user = self.request.user
        form = UpdateUserModelForm(self.request.POST, instance=get_user)
        if form.is_valid():
            form.save()
            messages.success(self.request, "ویرایش ذخیره شد")
            return redirect("home")

        return self.render_to_response(self.get_context_data(form=form))


def reSendVerifyCode(request, phone):
    get_user = get_object_or_404(User, phone=phone)
    if get_user.expire_verify_code.timestamp() < datetime.datetime.now().timestamp():
        get_user.save()
        # send(phone, get_user.verify_code),
        send_with_pattern(344666, phone, [get_user.verify_code]),

        return JsonResponse(
            data={"status": 200, "message": "کدفعالسازی ارسال شد"}, safe=False
        )
    return JsonResponse(data={"status": 404}, safe=False)


# ?import user data from excel
def import_user_data(request):
    print("run")
    import_data("apps/account_module/data/1.xlsx")
    import_data("apps/account_module/data/2.xlsx")

    return HttpResponse("import done ")
