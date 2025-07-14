from django.shortcuts import get_object_or_404
from apps.account_module.models import User
from melipayamak import Api
from django.conf import settings
import datetime

username = settings.MELI_USERNAME
password = settings.MELI_PASSWORD


def send_with_pattern(code, phone, text):
    api = Api(username, password)
    sms_soap = api.sms("soap")
    sms_soap.send_by_base_number(text, phone, code)


def send(phone, message):
    user = get_object_or_404(User, phone=phone)

    try:
        api = Api(username, password)
        sms = api.sms()
        to = f"{user.phone}"
        _from = "50004001033497"
        text = f" بیمه زائر :{message} - لغو11"
        response = sms.send(to, _from, text)
        print(response)
    except:
        print("sms have error")
