from flask import  Flask,render_template,redirect,request
import ibm_db
import re

app = Flask(__name__)

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
         stm=ibm_db.exec_immediate(con,qry)
         return "successfully registered"
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
         return "successfully registered"
     except Exception as e:
         print(e)
         return "registration failed"
@app.route("/validationusername",methods=["POST"])
def validateusername():
   unm=request.form["fname"]
   print(unm)
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


if __name__=="__main__":
    app.run(port=5001,debug=True)