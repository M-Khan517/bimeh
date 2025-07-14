from django.urls import path
from .views import index, HomeView, faq, ContactUsView, about_us, test

urlpatterns = [
    path("", index, name="index"),
    path("faq", faq, name="faq"),
    path(
        "home",
        HomeView.as_view(template_name="home_module/home.html"),
        name="home",
    ),
    path("contact-us", ContactUsView.as_view(), name="contact_us"),
    path("about-us", about_us, name="about_us"),
    path("test", test, name="test"),
]
