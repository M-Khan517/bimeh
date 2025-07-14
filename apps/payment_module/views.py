from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
import requests
import json
from django.contrib.auth.decorators import login_required
from apps.insurance_module.models import Insurance
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import PaymentLog
from utils.sender.send_sms import send, send_with_pattern


# ? sandbox merchant
if settings.SANDBOX:
    sandbox = "sandbox"
else:
    sandbox = "www"


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = (
    f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
)
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


amount = 0  # Rial / Required
description = "بیمه زائر"  # Required
phone = ""  # Optional
# Important: need to edit for realy server.
CallbackURL = "http://127.0.0.1:8000/py/verify/"


@login_required
def send_request(request: HttpRequest, code):
    if code is not None:
        get_user = request.user
        get_insurance = get_object_or_404(Insurance, code=code)

        if get_insurance.manager != get_user:
            return HttpResponseNotFound()
        else:
            request.session["insurance"] = {"code": code}
            phone = get_user.phone
            amount = get_insurance.total_price

    else:
        return HttpResponseNotFound()

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Phone": phone,
        "Description": description,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {"content-type": "application/json", "content-length": str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response["Status"] == 100:
                print(response)
                return redirect(ZP_API_STARTPAY + str(response["Authority"]))
            # {
            #     "status": True,
            #     "url": ZP_API_STARTPAY + str(response["Authority"]),
            #     "authority": response["Authority"],
            # }

            else:
                return JsonResponse({"status": False, "code": str(response["Status"])})
        return JsonResponse(response)

    except requests.exceptions.Timeout:
        return JsonResponse({"status": False, "code": "timeout"})
    except requests.exceptions.ConnectionError:
        return JsonResponse({"status": False, "code": "connection error"})


@login_required
def verify(request: HttpRequest):

    insurance_code = request.session["insurance"]["code"]

    if insurance_code is not None:
        get_insurance = get_object_or_404(Insurance, code=insurance_code)
        del request.session["insurance"]

        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": get_insurance.total_price,
            "Authority": request.GET.get("Authority"),
        }
        data = json.dumps(data)
        # set content length by data
        headers = {"content-type": "application/json", "content-length": str(len(data))}
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response["Status"] == 100:
                # return {"status": True, "RefID": response["RefID"]}

                context = {"status": True, "refId": response["RefID"]}
                get_insurance.pay_status = "1"
                get_insurance.pay_date = datetime.now()
                get_insurance.status = "1"

                get_insurance.save()

                PaymentLog(
                    insurance=get_insurance,
                    ref_id=response["RefID"],
                    pay_date=datetime.now(),
                    price=get_insurance.total_price,
                ).save()

                # send(
                #     request.user.phone,
                #     f"بیمه نامه با کد {get_insurance.code} در صف صدور است.",
                # )

                send_with_pattern(344668, request.user.phone, [get_insurance.code])

            else:
                # return {"status": False, "code": str(response["Status"])}
                context = {"status": False}

        return render(request, "payment_module/pay_status.html", context)
    else:
        return HttpResponseNotFound()
