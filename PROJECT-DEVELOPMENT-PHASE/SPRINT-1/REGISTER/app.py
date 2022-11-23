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
Settings={
    "productranking":"",
    "hubranking":"",
    "productalertkl":"",
     "productalertcnt":""
}
hub={
"listofhubs":[]
}
hubmanger={
  "ownername" : "",
  "hubname" : ""
}
otp={}
@app.route("/mainregister")
def Register():
    return render_template("Register.html")
@app.route("/subregister/<name>/<hubname>")
def Subregister(name,hubname):
    print(name)
    print(hubname)

    return render_template("subregister.html",name=name,hubname=hubname)
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

         rs=ObjectStorage.create_bucket(usernm)
         print(rs)
         if(rs != None):
             return "Registration failed due to invalid username please try again later"
         profile["userName"]=usernm
         profile["mailId"] = mailid
         profile["phNo"] = phno
         jsn=json.dumps(Settings)
         file=open(usernm+"settings","w")
         file.write(jsn)
         file.close()
         ObjectStorage.multi_part_upload(usernm,usernm+"settings",os.path.abspath(usernm+"settings"))
         os.remove(os.path.abspath(usernm+"settings"))
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
@app.route("/subvalidate/<name>/<hubname>",methods=["POST"])
def subregister(name,hubname):
     usernm=request.form["usernm"]
     mailid=request.form["mail"]
     phno=request.form["phno"]
     password=request.form["pass"]
     print(usernm)
     print(mailid)
     print(phno)
     print(password)
     try:
         con = ibm_db.connect(
             "DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fzn32689;PWD=bPKXp7YkTR3uKK3a",
             '', '')
         qry=f"INSERT INTO  FZN32689.REGISTRATION (USERNAME,MAILID,PHNO,PASSWORD,SUBUSER) VALUES('{usernm}','{mailid}','{phno}','{password}',1);"
         print(qry)

         rs = ObjectStorage.create_bucket(usernm)
         print(rs)
         if (rs != None):
             return "Registration failed due to invalid username please try again later"
         profile["userName"] = usernm
         profile["mailId"] = mailid
         profile["phNo"] = phno
         hubdetails=ObjectStorage.get_item(name,name+"hub")
         print(hubdetails)
         hubdetails=hubdetails.decode("UTF -8")
         data=json.loads(hubdetails)
         for x in data["listofhubs"]:
             if x["HubName"]==hubname:
                 hubmanger["hubname"]=hubname
                 hubmanger["ownername"]=name
                 hub["listofhubs"].append(hubmanger)
                 print(x["HubManager"]+"manager")
                 if x["HubManager"] != "":
                     print(x["HubManager"])
                     hubmanagerd = ObjectStorage.get_item(x["HubManager"], x["HubManager"] + "hub")
                     print(hubmanagerd)
                     hubmanagerd = hubmanagerd.decode("UTF -8")
                     hubmanagerd = json.loads(hubmanagerd)
                     for y in hubmanagerd["listofhubs"]:
                         if y["hubname"] == hubname:
                             hubmanagerd["listofhubs"].remove(y)
                             break
                     jsonm = json.dumps(hubmanagerd)
                     filem = open(x["HubManager"] + "hub", "w")
                     filem.write(jsonm)
                     filem.close()
                     ObjectStorage.multi_part_upload(x["HubManager"], x["HubManager"] + "hub",
                                                     os.path.abspath(x["HubManager"] + "hub"))
                     os.remove(os.path.abspath(x["HubManager"] + "hub"))
                     break
                 else:
                     x["HubManager"] = usernm
                     break
                 break

         jsn = json.dumps(Settings)
         file = open(usernm + "settings", "w")
         file.write(jsn)
         file.close()
         ObjectStorage.multi_part_upload(usernm, usernm + "settings", os.path.abspath(usernm + "settings"))
         os.remove(os.path.abspath(usernm + "settings"))
         fl = open(name + "hub", "w")
         fl.write(json.dumps(data))
         fl.close()
         ObjectStorage.multi_part_upload(name, name + "hub", os.path.abspath(name + "hub"))
         os.remove(os.path.abspath(name + "hub"))
         profile["settings"] = usernm + "settings"
         jsn1 = json.dumps(profile)
         jsn2 = json.dumps(hub)
         col1 = usernm + "profile"
         col2 = usernm + "hub"
         file = open(usernm + "profile", "w")
         file.write(jsn1)
         file.close()
         ObjectStorage.multi_part_upload(usernm, usernm + "profile", os.path.abspath(usernm + "profile"))
         os.remove(os.path.abspath(usernm + "profile"))
         file = open(usernm + "hub", "w")
         file.write(jsn2)
         file.close()
         ObjectStorage.multi_part_upload(usernm, usernm + "hub", os.path.abspath(usernm + "hub"))
         os.remove(os.path.abspath(usernm + "hub"))

         qry1 = f"INSERT INTO  FZN32689.SUBUSER (USERNAME,PROFILE,HUB) VALUES('{usernm}','{col1}','{col2}');"
         print(qry1)
         stm = ibm_db.exec_immediate(con, qry)
         stm = ibm_db.exec_immediate(con, qry1)
         MailVerfication.message(mailid,"Congratulations you account for managing the hub has been created ","Your username = "+usernm+" password = "+password)
         return "Registered Successfully"
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
        print(ot)
        print("matched")
        return "otp matched"
    print("mismatch")
    return "otp mismatch"

if __name__=="__main__":
    app.run(port=5001,debug=True,host="0.0.0.0")