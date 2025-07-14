from django.urls import include, path
from .views import (
    Insurances,
    SubUsers,
    remove_subuser,
    CreateSubUser,
    UpdateSubUser,
    GetInsuranceSubUsers,
    CreateInsurance,
    InsuranceStatus,
    generate_pdf,
    get_counties,
    generate_excel,
    GetInsurance,
    generate_pdf_for_manager,
    generate_excel_for_manager,
    get_subusers,
)
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("", Insurances.as_view(), name="insurances"),
    path("get/<code>", GetInsurance.as_view(), name="get-insurance"),
    path("create", CreateInsurance.as_view(), name="create_insurances"),
    path("sub-users", SubUsers.as_view(), name="sub_users"),
    path("sub-users/<code>", GetInsuranceSubUsers.as_view(), name="insurance_sub"),
    path("sub-users-insert", CreateSubUser.as_view(), name="create_sub"),
    path("sub-users/update/<id>", UpdateSubUser.as_view(), name="update_sub"),
    path("sub-users/delete/<id>", remove_subuser, name="remove_sub"),
    # region  download all subs for one user
    # download all user subsets
    path(
        "sub-users/export/pdf/<id>",
        generate_pdf_for_manager,
        name="manager_generate_pdf",
    ),
    path(
        "manager/export/excel/<id>",
        generate_excel_for_manager,
        name="manager_export_excel",
    ),
    # endregion
    # region  download subusers for one insurance
    # download subuser for insurance
    path("manager/export/<code>", generate_pdf, name="generate_pdf"),
    path("export/<insurance_id>", generate_excel, name="export"),
    # endregion
    path("status", InsuranceStatus.as_view(), name="status"),
    # region ajax
    path("get_counties/", get_counties, name="get_counties"),
    path("ajax/sub_users", get_subusers, name="ajax_subusers"),
    # endregion
]
