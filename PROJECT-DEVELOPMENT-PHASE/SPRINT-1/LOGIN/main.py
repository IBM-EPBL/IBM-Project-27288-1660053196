from flask import Flask,redirect,render_template,request

import ibm_db
import TwoStepAuthenticator
con=True
app=Flask(__name__)

otp={}
@app.route("/")
def Login():
    return render_template("Login.html")
@app.route("/validate" ,methods=["POST"])
def validate():
    print(type(request.form))
    usernm=request.form["usernm"]
    password=request.form["pass"]

    try:
        con = ibm_db.connect(
            "DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fzn32689;PWD=bPKXp7YkTR3uKK3a",
            '', '')
        try:
         qry=f"SELECT  * FROM FZN32689.REGISTRATION"
         stmt=ibm_db.exec_immediate(con,qry)
         result=ibm_db.fetch_both(stmt)
         while result!=False:
            if request.form.__contains__("sub"):
                if result["USERNAME"] == usernm and result["PASSWORD"] == password and result["SUBUSER"] == 1:
                    return redirect("http://127.0.0.1:5012/dashboard/"+usernm)
                else:
                    result = ibm_db.fetch_both(stmt)
            else:
             if result["USERNAME"]==usernm and  result["PASSWORD"]==password:
                return redirect("http://127.0.0.1:5002/dashboard/"+usernm)
             else:
                 result=ibm_db.fetch_both(stmt)

         return redirect("http://127.0.0.1:5000")

        except Exception as e:
            print(e)
            return redirect("http://127.0.0.1:5000")
    except Exception as e:
        print(e)
        return render_template("sorry.html")

@app.route("/uservalidate",methods=["POST"])
def validateusername():
    usr=request.form["fname"]
    try:
        con = ibm_db.connect(
            "DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fzn32689;PWD=bPKXp7YkTR3uKK3a",
            '', '')
        try:
            qry = f"SELECT  * FROM FZN32689.REGISTRATION"
            stmt = ibm_db.exec_immediate(con, qry)
            result = ibm_db.fetch_both(stmt)
            while result!=False:
                if(result["USERNAME"]==usr):
                    return ""
                else:
                    result = ibm_db.fetch_both(stmt)
            return "user not found"

        except:
            return "user not found"
    except:
        pass
@app.route("/passwordvalidate",methods=["POST"])
def validatepassword():
    password=request.form["pass"]
    username=request.form["name"]
    print(password)
    print(username)
    try:
        con = ibm_db.connect(
            "DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fzn32689;PWD=bPKXp7YkTR3uKK3a",
            '', '')
        try:
            qry = f"SELECT  * FROM FZN32689.REGISTRATION"
            stmt = ibm_db.exec_immediate(con, qry)
            result = ibm_db.fetch_both(stmt)
            while result!=False:
                if(result["USERNAME"]==username and result["PASSWORD"]==password):
                    otp[result["USERNAME"]]=TwoStepAuthenticator.generateOTP()
                    TwoStepAuthenticator.send_otp(result["MAILID"],otp[result["USERNAME"]])
                    return ""
                else:
                    result = ibm_db.fetch_both(stmt)
            return "incorrect password"

        except:
            return "incorrect password"
    except:
        pass
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
    app.run(debug=True)