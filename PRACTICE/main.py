from flask import Flask
import ibm_db
import ibm_boto3
from ibm_botocore.client import Config, ClientError
app=Flask(__name__)
dsn_hostname="21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
dsn_uid="fzn32689"
dsn_pwd="bPKXp7YkTR3uKK3a"
dsn_driver="{IBM DB2 ODBC DRIVER}"
dsn_databse="bludb"
dsn_port="31864"
dsn_protocol="TCPIP"
dsn_security = "SSL"
dsn=("DRIVER={0};"
     "DATABASE={1};"
     "HOSTNAME={2};"
     "PORT={3};"
     "PROTOCOL={4};"
     "UID={5};"
     "PWD={6};"
    "SECURITY={7};").format(dsn_driver,dsn_databse,dsn_hostname,dsn_port,dsn_protocol,dsn_uid,dsn_pwd,dsn_security)
print(dsn)
try:
    con=ibm_db.connect(dsn,"","")
    print("CONNECTED")

except:
    print("NOT ABLE TO CONNECT")

@app.route("/")
def fun():
    return "hello docker"