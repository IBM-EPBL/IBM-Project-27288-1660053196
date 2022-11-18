import sendgrid
from python_http_client.exceptions import HTTPError
import math,random

def send_otp(mailId,otp):
    API_KEY = "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"

    sg = sendgrid.SendGridAPIClient(API_KEY)
    data = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": mailId
                    }
                ],
                "subject": "OTP FROM INVENTORY MANAGEMENT SYSTEM IBM PROJECT"
            }
        ],
        "from": {
            "email": "bhawinjasperbj@gmail.com"
        },
        "content": [
            {
                "type": "text/plain",
                "value": "your otp don't share with any one " + otp
            }
        ]
    }
    try:
        response = sg.client.mail.send.post(request_body=data)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return ""
    except HTTPError as e:
        print(e.to_dict)
        return "INVALID MAILID"


def generateOTP():
    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

    # length of password can be changed
    # by changing value in range
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP
def message(mailId,subject,message):
    API_KEY = "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"

    sg = sendgrid.SendGridAPIClient(API_KEY)
    data = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": mailId
                    }
                ],
                "subject": subject
            }
        ],
        "from": {
            "email": "bhawinjasperbj@gmail.com"
        },
        "content": [
            {
                "type": "text/plain",
                "value": message
            }
        ]
    }
    try:
        response = sg.client.mail.send.post(request_body=data)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return ""
    except HTTPError as e:
        print(e.to_dict)
        return "INVALID MAILID"
