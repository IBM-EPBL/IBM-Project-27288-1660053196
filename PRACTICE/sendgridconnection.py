import sendgrid
from python_http_client.exceptions import HTTPError
import apikey


API_KEY=apikey.api_key

sg=sendgrid.SendGridAPIClient(API_KEY)
data = {
  "personalizations": [
    {
      "to": [
        {
          "email": "bhawinjasperofficial@gmail.com"
        }
      ],
      "subject": "Sending with SendGrid is Fun"
    }
  ],
  "from": {
    "email": "bhawinjasperbj@gmail.com"
  },
  "content": [
    {
      "type": "text/plain",
      "value": "and easy to do anywhere, even with Python"
    }
  ]
}
try:
 response = sg.client.mail.send.post(request_body=data)
 print(response.status_code)
 print(response.body)
 print(response.headers)
except HTTPError as e:
   print(e.to_dict)



