from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    logout_user,
    VerifyAccountView,
    ForgotPasswordView,
    ResetPassowrdView,
    UpdateUserView,
    reSendVerifyCode,
    import_user_data,
)

urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", logout_user, name="logout"),
    path("verify-account", VerifyAccountView.as_view(), name="verify_account"),
    # path("forgot-password", ForgotPasswordView.as_view(), name="forgot_password"),
    # path("reset-password", ResetPassowrdView.as_view(), name="reset_password"),
    path("update", UpdateUserView.as_view(), name="update_user"),
    path("resend/<phone>", reSendVerifyCode, name="resend"),
    path("import_data", import_user_data),
]
