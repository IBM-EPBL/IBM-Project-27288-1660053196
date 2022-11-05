from flask import  Flask,render_template,redirect,request
import ibm_db
import re
import ObjectStorage
import json
import os
import MailVerfication
app = Flask(__name__)
profile={
 "profileIamge":"",
  "userName": "",
   "mailId" :"",
    "phNo" :"",
    "settings" : ""
}
settings={
}
hub={
"listofhubs":[]
}
otp={}
@app.route("/mainregister")
def Register():
    return render_template("Register.html")
@app.route("/subregister")
def Subregister():
    return render_template("subregister.html")
@app.route("/mainvalidate",methods=["POST"])
def mainregister():
     usernm=request.form["usernm"]
     mailid=request.form["mail"]
     phno=request.form["phno"]
     password=request.form["pass"]
     try:
         con = ibm_db.connect(
             "DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fzn32689;PWD=bPKXp7YkTR3uKK3a",
             '', '')
         qry=f"INSERT INTO  FZN32689.REGISTRATION (USERNAME,MAILID,PHNO,PASSWORD,SUBUSER) VALUES('{usernm}','{mailid}','{phno}','{password}',0);"
         print(qry)

         ObjectStorage.create_bucket(usernm)
         profile["userName"]=usernm
         profile["mailId"] = mailid
         profile["phNo"] = phno
         jsn=json.dumps(settings)
         file=open(usernm+"-settings","w")
         file.write(jsn)
         file.close()
         ObjectStorage.multi_part_upload(usernm,usernm+"-settings",os.path.abspath(usernm+"-settings"))
         os.remove(os.path.abspath(usernm+"-settings"))
         profile["settings"]=usernm+"settings"
         jsn1=json.dumps(profile)
         jsn2=json.dumps(hub)
         col1=usernm+"profile"
         col2=usernm+"hub"
         file=open(usernm+"profile","w")
         file.write(jsn1)
         file.close()
         ObjectStorage.multi_part_upload(usernm,usernm+"profile",os.path.abspath(usernm+"profile"))
         os.remove(os.path.abspath(usernm+"profile"))
         file=open(usernm+"hub","w")
         file.write(jsn2)
         file.close()
         ObjectStorage.multi_part_upload(usernm,usernm+"hub",os.path.abspath(usernm+"hub"))
         os.remove(os.path.abspath(usernm+"hub"))

         qry1= f"INSERT INTO  FZN32689.MAINUSER (USERNAME,PROFILE,HUB) VALUES('{usernm}','{col1}','{col2}');"
         print(qry1)
         stm = ibm_db.exec_immediate(con, qry)
         stm=ibm_db.exec_immediate(con,qry1)
         return redirect("http://127.0.0.1:5000/")
     except Exception as e:
         print(e)
         return "registration failed"
@app.route("/subvalidate",methods=["POST"])
def subegister():
     usernm=request.form["usernm"]
     mailid=request.form["mail"]
     phno=request.form["phno"]
     password=request.form["pass"]
     try:
         con = ibm_db.connect(
             "DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fzn32689;PWD=bPKXp7YkTR3uKK3a",
             '', '')
         qry=f"INSERT INTO  FZN32689.REGISTRATION (USERNAME,MAILID,PHNO,PASSWORD,SUBUSER) VALUES('{usernm}','{mailid}','{phno}','{password}',1);"


         print(qry)
         stm=ibm_db.exec_immediate(con,qry)
         return redirect("http://127.0.0.1:5000/")
     except Exception as e:
         print(e)
         return "registration failed"
@app.route("/validationusername",methods=["POST"])
def validateusername():
   unm=request.form["fname"]
   try:
    con = ibm_db.connect(
        "DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fzn32689;PWD=bPKXp7YkTR3uKK3a",
        '', '')
    qry = f"SELECT  * FROM FZN32689.REGISTRATION"
    stmt = ibm_db.exec_immediate(con, qry)
    result = ibm_db.fetch_both(stmt)
    while result!=False:
        if(result["USERNAME"]==unm):
            return "USER ALREADY EXIST"
        else:
            result = ibm_db.fetch_both(stmt)
            print(unm)

   except:
       print("something went wrong")
   return ""
@app.route("/validationmailid",methods=["POST"])
def validatemailid():
    unm = request.form["fname"]
    if(unm == ""):
        return "INVALID MAIL ID"
    try:
        con = ibm_db.connect(
            "DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fzn32689;PWD=bPKXp7YkTR3uKK3a",
            '', '')
        qry = f"SELECT  * FROM FZN32689.REGISTRATION"
        stmt = ibm_db.exec_immediate(con, qry)
        result = ibm_db.fetch_both(stmt)
        while result != False:
            if (result["MAILID"] == unm):
                return "USER ALREADY EXIST"
            else:
                result = ibm_db.fetch_both(stmt)
        otp[unm]=MailVerfication.generateOTP()
        print(otp)
        return MailVerfication.send_otp(unm,otp[unm])

    except:
        print("something went wrong")
    return ""
@app.route("/validationphno",methods=["POST"])
def validatephno():
    unm = request.form["fname"]
    if (len(unm) != 10):
        return "INVALID PHONE NUMBER"

    try:
        con = ibm_db.connect(
            "DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fzn32689;PWD=bPKXp7YkTR3uKK3a",
            '', '')
        qry = f"SELECT  * FROM FZN32689.REGISTRATION"
        stmt = ibm_db.exec_immediate(con, qry)
        result = ibm_db.fetch_both(stmt)

        while result != False:
            if (result["PHNO"] == unm):
                return "USER ALREADY EXIST"
            else:
                result = ibm_db.fetch_both(stmt)

    except:
        print("something went wrong")
    return ""
@app.route("/psck",methods=["POST"])
def passwordchecker():
    passwd = request.form["fname"]
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"

    # compiling regex
    pat = re.compile(reg)

    # searching regex
    mat = re.search(pat, passwd)

    # validating conditions
    if mat:
        return ""
    else:
        return "password should contain 6 to 20 characters,one special symbol,at least one uppercase and one lowercase character, at least one number"

@app.route("/verifyotp",methods=["POST"])
def verifyotp():
    print("hii fro verifier of otp")
    mail=request.form["mail"]
    ot=request.form["otp"]
    print(mail)
    print(ot)
    if otp[mail]== ot:
        print("matched")
        return "otp matched"
    print("mismatch")
    return "otp mismatch"
if __name__=="__main__":
    app.run(port=5001,debug=True)