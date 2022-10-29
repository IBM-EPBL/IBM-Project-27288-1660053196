import sendgrid
from sendgrid.helpers.mail import *
import json
import urllib.request

file=urllib.request.urlopen("https://jasper.s3.jp-tok.cloud-object-storage.appdomain.cloud/sample.json")

data=json.load(file)
print(data["bhawin"])


