from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from web_project import TemplateLayout
from .models import AboutUs, CategoryFAQ, Gallery, SettingSite
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ContactUsModelForm
from django.contrib.messages import success
from django.contrib.auth.decorators import login_required


def index(request):

    setting = None
    about_us = None

    if SettingSite.objects.exists():
        setting = SettingSite.objects.first()
        request.session["setting"] = {
            "logo": setting.logo.url if setting.logo else None,
            "name": setting.name if setting.name else None,
            "phone": setting.phone if setting.phone else None,
            "email": setting.email if setting.email else None,
        }

    if AboutUs.objects.exists():
        about_us = AboutUs.objects.first()
        request.session["about"] = {"about_us": about_us.text}

    return render(request, "home_module/index.html")


# after login view


class HomeView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        print(self.request.user.is_authenticated)
        get_user = self.request.user

        if get_user.insurances.exists():

            insurances = get_user.insurances.all()

            total = 0
            total_paid = 0

            for insurance in insurances:
                if insurance.status != "0":
                    total_paid += int(insurance.total_price)

                total += int(insurance.total_price)

            subs = get_user.sub_users.all()

            context["total"] = total
            context["total_paid"] = total - total_paid
            context["paid"] = total_paid
            context["insurance_count"] = insurances.filter(status="2").count()
            context["sub_count"] = subs.count()

            if subs.count() > 3:
                context["subs"] = subs[:3]
            else:
                context["subs"] = subs

        return context


def faq(request):

    categories = CategoryFAQ.objects.all()
    setting = None
    try:
        setting = SettingSite.objects.all()[0]
    except:
        setting = None

    context = {"categories": categories, "contact": setting}

    return render(request, "home_module/FAQ.html", context)


class ContactUsView(View):
    def get(self, request):
        form = ContactUsModelForm()
        context = {"form": form}
        return render(request, "home_module/contact_us.html", context)

    def post(self, request):
        form = ContactUsModelForm(request.POST)
        if form.is_valid():
            form.save()
            success(request, "ثبت شد")
            return render(request, "home_module/contact_us.html")
        else:
            return render(request, "home_module/contact_us.html", {"form": form})


def about_us(request):
    gallery = Gallery.objects.filter(show_in_aboutUs=True)
    about = AboutUs.objects.first()

    context = {"gallery": gallery, "about": about}

    return render(request, "home_module/about_us.html", context)


def test(request: HttpRequest):
    return HttpResponse(request.user)
