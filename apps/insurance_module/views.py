from datetime import datetime
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
import openpyxl
import openpyxl.workbook
from iranian_cities.models import Province, County
from utils.pdf_generator.generate import generate_pdf_file
from django.db.models import Q
from web_project import TemplateLayout
from .models import Insurance, InsurancePrice
from django.http import (
    FileResponse,
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    JsonResponse,
)
from apps.account_module.models import SubUser, User
from .forms import (
    CreateSubUserForm,
    UpdateSubUserModelForm,
    CreateInsuranceForm,
    SearchSubsForm,
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from iranian_cities.models import County
import json


# Create your views here.


class Insurances(LoginRequiredMixin, TemplateView):
    template_name = "insurance_module/index.html"

    def get_context_data(self, **kwargs):

        get_user = self.request.user

        insurances = get_user.insurances.all()

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context["insurances"] = insurances

        return context


class CreateInsurance(LoginRequiredMixin, TemplateView):
    template_name = "insurance_module/createInsurance.html"

    def get_context_data(self, **kwargs):

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        user = self.request.user

        now = datetime.now()
        subsets = SubUser.objects.filter(manager=user).all()
        subsets = subsets.filter(Q(insurances__end_date__lt=now) | Q(insurances=None))

        if subsets.count() > 0:
            context["subs"] = subsets.all()

        if not "form" in context:
            context["form"] = CreateInsuranceForm()

        return context

    def post(self, request, **kwargs):
        user = request.user
        form = CreateInsuranceForm(request.POST)

        if form.is_valid():

            now = datetime.now()
            subsets = SubUser.objects.filter(manager=user).all()
            subsets = subsets.filter(
                Q(insurances__end_date__lt=now) | Q(insurances=None)
            )

            insurance_maneger = form.cleaned_data.get("insurance_maneger")

            if subsets.count() == 0 and insurance_maneger == False:
                form.add_error(
                    "insurance_maneger", "تعداد بیمه شوندگان کمتر از یک نفر است"
                )
            else:

                destination = form.cleaned_data.get("destination")

                start_date = form.cleaned_data.get("start_date")

                end_date = form.cleaned_data.get("end_date")

                province = form.cleaned_data.get("province")

                county = form.cleaned_data.get("county")

                insuranceprice = InsurancePrice.objects.all()[0]

                new_insurance = Insurance(
                    manager=user,
                    insuranceprice=insuranceprice,
                    destination=destination,
                    origin_province=province,
                    origin_county=county,
                    start_date=start_date,
                    end_date=end_date,
                    insurance_maneger=insurance_maneger,
                )

                new_insurance.save()

                new_insurance.subsets.set(subsets)

                messages.success(self.request, "درخواست بیمه ثبت شد")

                return redirect("get-insurance", code=new_insurance.code)

        return self.render_to_response(self.get_context_data(form=form))


class GetInsurance(LoginRequiredMixin, TemplateView):
    template_name = "insurance_module/insurance.html"

    def get_context_data(self, **kwargs):

        insurance = get_object_or_404(Insurance, code=kwargs["code"])
        subsets = insurance.subsets.all()

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context["insurance"] = insurance
        context["subsets"] = subsets

        return context


class SubUsers(LoginRequiredMixin, TemplateView):
    template_name = "insurance_module/sub_users.html"

    def get_context_data(self, **kwargs):

        get_user = self.request.user

        sub_users = get_user.sub_users.all()

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        if not "page_obj" in context:

            paginator = Paginator(sub_users, 10)

            page_number = self.request.GET.get("page")

            page_obj = paginator.get_page(page_number)

            context["page_obj"] = page_obj
            context["user"] = get_user

        if not "form" in context:

            context["form"] = SearchSubsForm()

        return context

    def post(self, request, **kwargs):

        form = SearchSubsForm(request.POST)

        if form.is_valid():

            get_user = self.request.user

            full_name = form.cleaned_data.get("full_name")

            national_code = form.cleaned_data.get("national_code")

            sub_users: SubUser = get_user.sub_users.all()

            sub_users = sub_users.filter(
                Q(full_name__contains=full_name)
                & Q(national_code__contains=national_code)
            )

            paginator = Paginator(sub_users, 10)

            page_number = self.request.GET.get("page")

            page_obj = paginator.get_page(page_number)

            return self.render_to_response(
                self.get_context_data(form=form, page_obj=page_obj)
            )


class GetInsuranceSubUsers(LoginRequiredMixin, TemplateView):
    template_name = "insurance_module/insurance_subUser.html"

    def get_context_data(self, **kwargs):

        insurance = get_object_or_404(Insurance, code=kwargs["code"])

        sub_users = insurance.subsets.all()

        paginator = Paginator(sub_users, 10)

        page_number = self.request.GET.get("page")

        page_obj = paginator.get_page(page_number)

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context["page_obj"] = page_obj

        context["insurance"] = insurance

        return context


class CreateSubUser(LoginRequiredMixin, TemplateView):
    template_name = "insurance_module/create_sub_user.html"

    def get_context_data(self, **kwargs):

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        if not "form" in context:
            context["form"] = CreateSubUserForm()

        return context

    def post(self, request, *args, **kwargs):
        form = CreateSubUserForm(request.POST)
        if form.is_valid():
            national_code = form.cleaned_data.get("national_code")

            check_nationalCode = SubUser.objects.filter(
                national_code=national_code
            ).exists()

            if check_nationalCode:
                form.add_error("national_code", "کد ملی تکراری است.")
            else:
                SubUser.objects.create(
                    full_name=form.cleaned_data.get("full_name"),
                    national_code=national_code,
                    manager=request.user,
                )
                messages.success(request, "زیر مجموعه ایجاد شد")
                return redirect("sub_users")

        return self.render_to_response(self.get_context_data(form=form))


def remove_subuser(request: HttpRequest, id):
    user = request.user

    sub = get_object_or_404(SubUser, id=id)

    check_user_and_usersub = user.sub_users.filter(id=id).exists()

    if check_user_and_usersub:
        SubUser.delete(sub)
        return redirect("sub_users")
    else:
        return HttpResponseNotFound()


class UpdateSubUser(LoginRequiredMixin, TemplateView):
    template_name = "insurance_module/update_sub_user.html"

    def get_context_data(self, **kwargs):

        subuser = get_object_or_404(SubUser, id=kwargs.get("id"))

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        if not "form" in context:
            context["form"] = UpdateSubUserModelForm(instance=subuser)
        context["id"] = subuser.id

        return context

    def post(self, request, *args, **kwargs):
        subuser = get_object_or_404(SubUser, id=kwargs.get("id"))

        form = UpdateSubUserModelForm(request.POST, instance=subuser)

        if form.is_valid():
            form.save()

            messages.success(request, "ویرایش با موفقیت انجام شد")
            return redirect("sub_users")

        form = UpdateSubUserModelForm(request.POST, instance=subuser)
        return self.render_to_response(self.get_context_data(form=form))


class InsuranceStatus(LoginRequiredMixin, TemplateView):
    template_name = "insurance_module/InsuranceStatus.html"

    def get_context_data(self, **kwargs):

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        get_user = self.request.user

        insurances = get_user.insurances.all()

        context["unpaids"] = insurances.filter(status=0)
        context["checks"] = insurances.filter(status=1)
        context["checkeds"] = insurances.filter(status=2)
        context["rejects"] = insurances.filter(status=3)

        context["insurances"] = insurances

        return context


def generate_pdf(request, code):

    insurance = get_object_or_404(Insurance, code=code)

    sub_users = insurance.subsets.all()

    buffer = generate_pdf_file(code, sub_users)

    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="subsets_{code}.pdf"'

    # response = FileResponse(
    #     generate_pdf_file(insurance.code, sub_users),
    #     as_attachment=True,
    #     filename=f"subsets_{insurance.code}.pdf",
    # )
    return response


def generate_pdf_for_manager(request, id):

    manager = get_object_or_404(User, id=id)

    sub_users = manager.sub_users.all()

    buffer = generate_pdf_file(None, sub_users)

    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="subsets_{manager.national_code}.pdf"'
    )

    # response = FileResponse(
    #     generate_pdf_file(None, sub_users),
    #     as_attachment=True,
    #     filename=f"subsets_{manager.national_code}.pdf",
    # )
    return response


def generate_excel(request, insurance_id):
    insurance = get_object_or_404(Insurance, id=insurance_id)
    subs = insurance.subsets.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "subs"

    ws.append(["نام و نام خانوادگی", "کدملی"])

    if insurance.insurance_maneger:
        ws.append([insurance.manager.full_name, insurance.manager.national_code])

    for sub in subs:
        ws.append([sub.full_name, sub.national_code])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        f"attachment; filename=insurance_{insurance.code}.xlsx"
    )

    wb.save(response)
    return response


def generate_excel_for_manager(request, id):
    manager = get_object_or_404(User, id=id)
    subs = manager.sub_users.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "subs"

    ws.append(["نام و نام خانوادگی", "کدملی"])

    for sub in subs:
        ws.append([sub.full_name, sub.national_code])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        f"attachment; filename=insurance_{manager.national_code}.xlsx"
    )

    wb.save(response)
    return response


# ajax


def get_counties(requst):
    province_id = requst.GET.get("province_id")

    counties = County.objects.filter(province_id=province_id).values("id", "name")

    return JsonResponse(list(counties), safe=False)


def get_subusers(request: HttpRequest):
    if request.method == "GET":
        if request.GET.get("manager_id"):
            manager_id = request.GET.get("manager_id")

            find_user = get_object_or_404(User, id=manager_id)

            data = list(find_user.sub_users.all().values("id", "national_code"))

            return JsonResponse(data, safe=False)
