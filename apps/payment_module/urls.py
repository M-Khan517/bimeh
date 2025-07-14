from django.urls import path
from .views import verify, send_request

urlpatterns = [
    path("request/<code>", send_request, name="request"),
    path("verify/", verify, name="verify"),
]
