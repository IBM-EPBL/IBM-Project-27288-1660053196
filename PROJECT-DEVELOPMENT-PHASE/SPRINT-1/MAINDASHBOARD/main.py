from flask import Flask,render_template,request,redirect
import json
import PIL.Image as Image
import io
import os
import ObjectStorage
import ibm_db
import TwoStepAuthenticator
import  re

app = Flask(__name__)
Hntry={
    "HubName" :"",
    "HubLocation" :"",
    "HubManager":"",
    "ProductDetails":[],
    "SupplierDetails" :[]
}
Pdetails={
"productname" :"",
"suppliername" :"",
"pricedetails" :[]
}
pricedetails={
    "productprice":"",
    "sellingprice":"",
    "date":"",
    "qty":""
}
Sdetails={
   "suppliername":"",
    "supplierlocation" :"",
    "suppliedproducts":""

}
otp={}
@app.route("/dashboard/<name>")
def dashboard(name):
   data={name:"you can da "+name}
   return render_template("MainBoard.html",name=name,data=json.dumps(data))
@app.route("/profile/<name>")
def profile(name):
    b=ObjectStorage.get_item(name,name+"profile")
    print(b)
    b=b.decode("UTF-8")
    data=json.loads(b)
    return  render_template("profile.html",name=name,data=data)
@app.route("/Analysis/<name>")
def Analysis(name):
    return  render_template("Analysis.html",name=name)
@app.route("/Ranking/<name>")
def Ranking(name):
    return  render_template("Ranking.html",name=name)
@app.route("/HubEntry/<name>")
def HubEntry(name):
    return  render_template("HubEntry.html",name=name)
@app.route("/HubDashBoard/<name>")
def HubDashBoard(name):
    return  render_template("HubDashBoard.html",name=name)
@app.route("/changeprofile/<name>",methods=["POST"])
def changeprofile(name):
   by=request.files['file']
   by.save(by.filename)
   ObjectStorage.multi_part_upload(name,name+"profilepic",os.path.abspath(by.filename))
   os.remove(by.filename)
   b = ObjectStorage.get_item(name, name + "profile")
   print(b)
   b = b.decode("UTF-8")
   data = json.loads(b)
   print(type(data))
   data1=data
   data1["profileImage"]=name+"profilepic"
   print(data1["profileImage"])

   print(data1)
   fl=open(name + "profile","w")
   fl.write(json.dumps(data1))
   fl.close()
   ObjectStorage.multi_part_upload(name, name + "profile", os.path.abspath(name + "profile"))
   os.remove(os.path.abspath(name + "profile"))
   return render_template("profile.html", name=name, data=data)
@app.route("/navforhubentry/<name>",methods=["POST"])
def navforhubentry(name):
    navnm=request.form["fname"]
    if(navnm=="Add Hub"):
     return render_template("addHub.html",name=name)
    if (navnm == "AddProductDetails"):
        return render_template("addProduct.html",name=name)
    if (navnm == "AddSupplierDetails"):
        return render_template("addSupplier.html",name=name)
    if (navnm == "Hub's"):
        return render_template("Hub's.html",name=name)
    if (navnm == "ProductDetails"):
        return render_template("Productdetails.html",name=name)
    if (navnm == "SupplierDetails"):
        return render_template("Supplierdetails.html",name=name)

@app.route("/hubentry/<name>",methods=["POST"])
def hubentry(name):
    hname=request.form["hname"]
    hloc=request.form["hloc"]
    print(hname)
    print(hloc)
    by=ObjectStorage.get_item(name,name+"hub")
    print(by)
    b = by.decode("UTF-8")
    data = json.loads(b)
    print(type(data))
    Hntry["HubName"]=str(hname)
    Hntry["HubLocation"]=str(hloc)
    data["listofhubs"].append(Hntry)
    print(data)
    f=open(name+"hub","w")
    f.write(json.dumps(data))
    f.close()
    ObjectStorage.multi_part_upload(name,name+"hub",os.path.abspath(name+"hub"))
    os.remove(os.path.abspath(name+"hub"))
    return render_template("HubEntry.html", name=name)
@app.route("/gethublist/<name>",methods=["POST"])
def hublist(name):
    by = ObjectStorage.get_item(name, name + "hub")
    print(by)
    b = by.decode("UTF-8")
    return b
@app.route("/addproduct/<name>",methods=["POST"])
def addproduct(name):
    pname=request.form["pname"]
    sname=request.form["sname"]
    price=request.form["price"]
    sprice=request.form["sprice"]
    qty=request.form["qty"]
    date=request.form["date"]
    hub=request.form["hub"]
    by = ObjectStorage.get_item(name, name + "hub")
    by = by.decode("UTF-8")
    data = json.loads(by)
    print(data)

    for x in data["listofhubs"]:
        if x["HubName"] == hub:
          print(x)

          for y in  x["ProductDetails"]:
              print(y)
              if y["productname"] ==pname and  y["suppliername"]==sname:
                  pricedetails["productprice"]=price
                  pricedetails["sellingprice"]=sprice
                  pricedetails["date"]=date
                  pricedetails["qty"]=qty
                  x["HubName"]["ProductDetails"]["pricedetails"].append(pricedetails)
                  break
              else:
                  Pdetails["productname"] = pname
                  Pdetails["suppliername"] = sname
                  pricedetails["productprice"] = price
                  pricedetails["sellingprice"] = sprice
                  pricedetails["date"] = date
                  pricedetails["qty"] = qty
                  Pdetails["pricedetails"].append(pricedetails)
                  x["ProductDetails"].append(Pdetails)
                  break
          if len(x["ProductDetails"]) == 0 :
              Pdetails["productname"] = pname
              Pdetails["suppliername"] = sname
              pricedetails["productprice"] = price
              pricedetails["sellingprice"] = sprice
              pricedetails["date"] = date
              pricedetails["qty"] = qty
              Pdetails["pricedetails"].append(pricedetails)
              x["ProductDetails"].append(Pdetails)
              break
          break

    print(data)
    f = open(name + "hub", "w")
    f.write(json.dumps(data))
    f.close()
    ObjectStorage.multi_part_upload(name, name + "hub", os.path.abspath(name + "hub"))
    print(data)
    os.remove(os.path.abspath(name + "hub"))

    return  render_template("HubEntry.html",name=name)
@app.route("/addsupplier/<name>",methods=["POST"])
def addsupplier(name):
    hub = request.form["hub"]
    sname = request.form["sname"]
    sloc = request.form["sloc"]
    soty = request.form["qty"]
    Sdetails["suppliername"]=sname
    Sdetails["supplierlocation"]=sloc
    Sdetails["suppliedproducts"]=soty
    by=ObjectStorage.get_item(name,name+"hub")
    by=by.decode("UTF-8")
    data=json.loads(by)
    print(data)
    for x in data["listofhubs"]:
        if x["HubName"] == hub:
          x["SupplierDetails"].append(Sdetails)
          break
    f = open(name + "hub", "w")
    f.write(json.dumps(data))
    f.close()
    ObjectStorage.multi_part_upload(name, name + "hub", os.path.abspath(name + "hub"))
    print(data)
    os.remove(os.path.abspath(name + "hub"))
    return  render_template("HubEntry.html",name=name)
@app.route("/productdetails/<name>",methods=["POST"])
def productdetails(name):
    hubname=request.form["fname"]
    print(hubname)
    by = ObjectStorage.get_item(name, name + "hub")
    print(by)
    b = by.decode("UTF-8")
    data=json.loads(b)
    senddata = ""
    for x in data["listofhubs"]:
        if x["HubName"] == hubname:
            senddata = json.dumps(x["ProductDetails"])
            print(senddata)
    return senddata
@app.route("/supplierdetails/<name>",methods=["POST"])
def supplierdetails(name):
    hubname=request.form["fname"]
    print(hubname)
    by = ObjectStorage.get_item(name, name + "hub")
    print(by)
    b = by.decode("UTF-8")
    data=json.loads(b)
    senddata=""
    for x in data["listofhubs"]:
        if x["HubName"]==hubname:
            senddata=json.dumps(x["SupplierDetails"])
    return senddata
@app.route("/changepassword/<name>")
def changepassword(name):
    print(name)
    return render_template("passwordchange.html",name=name)
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
        return "something went wrong"
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
@app.route("/passwordchange/<name>",methods=["POST"])
def changed(name):
    newpas=request.form["pass"]
    print(newpas)

    try:
        con = ibm_db.connect(
            "DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fzn32689;PWD=bPKXp7YkTR3uKK3a",
            '', '')
        qry1 = f"SELECT  * FROM FZN32689.REGISTRATION"
        stmt = ibm_db.exec_immediate(con, qry1)
        qry = ""
        result = ibm_db.fetch_both(stmt)
        username=""
        mailid=""
        phno=""
        subuser=""
        while result != False:
            if result["USERNAME"]==name:
                username=result['USERNAME']
                mailid=result['MAILID']
                phno=result['PHNO']
                subuser=result['SUBUSER' ]
                qry=f"UPDATE FZN32689.REGISTRATION SET  'USERNAME' = '{username}',  'MAILID' = '{mailid}',  'PHNO' = '{phno}', 'PASSWORD' = '{newpas}',  'SUBUSER' = '{subuser}' WHERE 'USERNAME' = '{name}';"

                break
            else:
                result=ibm_db.fetch_both(stmt)
        stmt = ibm_db.exec_immediate(con, qry)
    except Exception as e:
        print(e)
        return "Something went wrong"
    return redirect("http://127.0.0.1:5002/profile/"+name)
if __name__=="__main__":
    app.run(port=5002,debug=True)


