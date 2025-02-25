import requests
import base64

from datetime import datetime
from requests.auth import HTTPBasicAuth

from django.shortcuts import render, get_object_or_404
from django.conf import settings

from orders.models import Order
from .tasks import payment_complete

business_shortcode = settings.BUSINESS_SHORTCODE
passkey = settings.PASSKEY
timestamp = settings.TIMESTAMP

def get_access_token():
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    consumer_secret = settings.CONSUMER_SECRET
    consumer_key = settings.CONSUMER_KEY

    res = requests.get(
        api_url,
        auth=HTTPBasicAuth(consumer_key, consumer_secret)
    )
    token = res.json()['access_token']
    return token

def generate_password():
    """Generates mpesa api password using the provided shortcode and passkey"""

    password_str = str(business_shortcode) + str(passkey) + str(timestamp)
    password_bytes = password_str.encode("ascii")
    return base64.b64encode(password_bytes).decode("utf-8")

def payment_completed(request):
    return render(request, 'payment/completed')

def payment_cancelled(request):
    return render(request, 'payment/canceled')

def payment_process(request):
    # uncomment code to handle mpesa payment tests
    order_id = request.session.get('order_id')
    order = get_object_or_404(
        Order, id=order_id
    )
    business_credentials = generate_password()
    callback_url = "https://d40e-102-209-76-53.ngrok-free.app"
    checkout_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    access_token = get_access_token()
    headers = { "Authorization": f"Bearer {access_token}" ,"Content-Type": "application/json" }

    req_data = {
        "BusinessShortCode": business_shortcode,    
        "Password": business_credentials,    
        "Timestamp": timestamp ,    
        "TransactionType": "CustomerPayBillOnline",    
        "Amount": "1",    
        "PartyA": "254113460935",    
        "PartyB":"174379",    
        "PhoneNumber":"254113460935",    
        "CallBackURL": callback_url,    
        "AccountReference":"TestPayment",
        "TransactionDesc":"TestPayment"
    }

    res = requests.post(
        checkout_url, json=req_data, headers=headers, timeout=30
    )

    res_data = res.json()
    if res_data['ResponseCode'] == 0:
        order.paid = True
        order.payment = res_data['MerchantRequestId']
        payment_completed.delay(order.id)
        order.save()


    return render(request, 'payment/process.html')