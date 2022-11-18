from flask import Flask, render_template, request, redirect
import json
import PIL.Image as Image
import io
import os
import ObjectStorage
import ibm_db
import TwoStepAuthenticator
import re

app = Flask(__name__)
Hntry = {
    "HubName": "",
    "HubLocation": "",
    "HubManager": "",
    "ProductDetails": [],
    "SupplierDetails": []
}
Pdetails = {
    "productname": "",
    "suppliername": "",
    "pricedetails": [],
    "salesdetails": []
}
pricedetails = {
    "productprice": "",
    "sellingprice": "",
    "date": "",
    "qty": ""
}
sales = {
    "saledqty": "",
    "saleddate": "",

}

Sdetails = {
    "suppliername": "",
    "supplierlocation": "",
    "suppliedproducts": ""

}
Settings={
    "productranking":"",
    "hubranking":"",
    "productalertkl":"",
     "productalertcnt":""
}
otp = {}


@app.route("/dashboard/<name>")
def dashboard(name):
    data = {name: "you can da " + name}
    return render_template("MainBoard.html", name=name, data=json.dumps(data))


@app.route("/profile/<name>")
def profile(name):
    b = ObjectStorage.get_item(name, name + "profile")
    print(b)
    b = b.decode("UTF-8")
    data = json.loads(b)
    return render_template("profile.html", name=name, data=data)


@app.route("/Analysis/<name>")
def Analysis(name):
    return render_template("Analysis.html", name=name)


@app.route("/Ranking/<name>")
def Ranking(name):
    return render_template("Ranking.html", name=name)


@app.route("/HubEntry/<name>")
def HubEntry(name):
    return render_template("HubEntry.html", name=name)


@app.route("/HubDashBoard/<name>")
def HubDashBoard(name):
    return render_template("HubDashBoard.html", name=name)


@app.route("/changeprofile/<name>", methods=["POST"])
def changeprofile(name):
    by = request.files['file']
    by.save(by.filename)
    ObjectStorage.multi_part_upload(name, name + "profilepic", os.path.abspath(by.filename))
    os.remove(by.filename)
    b = ObjectStorage.get_item(name, name + "profile")
    print(b)
    b = b.decode("UTF-8")
    data = json.loads(b)
    print(type(data))
    data1 = data
    data1["profileImage"] = name + "profilepic"
    print(data1["profileImage"])

    print(data1)
    fl = open(name + "profile", "w")
    fl.write(json.dumps(data1))
    fl.close()
    ObjectStorage.multi_part_upload(name, name + "profile", os.path.abspath(name + "profile"))
    os.remove(os.path.abspath(name + "profile"))
    return render_template("profile.html", name=name, data=data)


@app.route("/navforhubentry/<name>", methods=["POST"])
def navforhubentry(name):
    navnm = request.form["fname"]
    if (navnm == "Add Hub"):
        return render_template("addHub.html", name=name)
    if (navnm == "AddProductDetails"):
        return render_template("addProduct.html", name=name)
    if (navnm == "AddSupplierDetails"):
        return render_template("addSupplier.html", name=name)
    if (navnm == "Hub's"):
        return render_template("Hub's.html", name=name)
    if (navnm == "ProductDetails"):
        return render_template("Productdetails.html", name=name)
    if (navnm == "SupplierDetails"):
        return render_template("Supplierdetails.html", name=name)


@app.route("/hubentry/<name>", methods=["POST"])
def hubentry(name):
    hname = request.form["hname"]
    hloc = request.form["hloc"]
    print(hname)
    print(hloc)
    by = ObjectStorage.get_item(name, name + "hub")
    print(by)
    b = by.decode("UTF-8")
    data = json.loads(b)
    print(type(data))
    Hntry["HubName"] = str(hname)
    Hntry["HubLocation"] = str(hloc)
    data["listofhubs"].append(Hntry)
    print(data)
    f = open(name + "hub", "w")
    f.write(json.dumps(data))
    f.close()
    ObjectStorage.multi_part_upload(name, name + "hub", os.path.abspath(name + "hub"))
    os.remove(os.path.abspath(name + "hub"))
    return render_template("HubEntry.html", name=name)


@app.route("/gethublist/<name>", methods=["POST"])
def hublist(name):
    b = ObjectStorage.get_item(name, name + "hub")
    print(b)
    b = b.decode("UTF-8")
    b=json.loads(b)
    rtdata=[]
    for x in b["listofhubs"]:
        by=ObjectStorage.get_item(x["ownername"],x["ownername"]+"hub")
        print(by)
        by=by.decode("UTF -8")
        by=json.loads(by)
        for y in by["listofhubs"]:
            if y["HubName"] == x["hubname"]:
                rtdata.append(y)
    return json.dumps(rtdata)


@app.route("/addproduct/<name>", methods=["POST"])
def addproduct(name):
    pname = request.form["pname"]
    sname = request.form["sname"]
    price = request.form["price"]
    sprice = request.form["sprice"]
    qty = request.form["qty"]
    date = request.form["date"]
    hub = request.form["hub"]
    by = ObjectStorage.get_item(name, name + "hub")
    by = by.decode("UTF-8")
    data = json.loads(by)
    print(data)

    for x in data["listofhubs"]:
        if x["hubname"] == hub:
            print(x)
            nw=x
            by=ObjectStorage.get_item(x['ownername'],x['ownername']+"hub")
            by=by.decode("UTF -8")
            by=json.loads(by)
            for t in by["listofhubs"]:
                if t["HubName"] == hub:
                    x=t
            for y in x["ProductDetails"]:
                print(y)
                if y["productname"] == pname and y["suppliername"] == sname:
                    pricedetails["productprice"] = price
                    pricedetails["sellingprice"] = sprice
                    pricedetails["date"] = date
                    pricedetails["qty"] = qty
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
            if len(x["ProductDetails"]) == 0:
                Pdetails["productname"] = pname
                Pdetails["suppliername"] = sname
                pricedetails["productprice"] = price
                pricedetails["sellingprice"] = sprice
                pricedetails["date"] = date
                pricedetails["qty"] = qty
                Pdetails["pricedetails"].append(pricedetails)
                x["ProductDetails"].append(Pdetails)
            print(by)
            file=open(nw['ownername']+"hub","w")
            file.write(json.dumps(by))
            file.close()
            ObjectStorage.multi_part_upload(nw['ownername'],nw['ownername']+"hub", os.path.abspath(nw['ownername']+"hub"))
            print(data)
            os.remove(os.path.abspath(nw['ownername']+"hub"))

            break

    print(data)
    f = open(name + "hub", "w")
    f.write(json.dumps(data))
    f.close()
    ObjectStorage.multi_part_upload(name, name + "hub", os.path.abspath(name + "hub"))
    print(data)
    os.remove(os.path.abspath(name + "hub"))

    return render_template("HubEntry.html", name=name)


@app.route("/addsupplier/<name>", methods=["POST"])
def addsupplier(name):
    hub = request.form["hub"]
    sname = request.form["sname"]
    sloc = request.form["sloc"]
    soty = request.form["qty"]
    Sdetails["suppliername"] = sname
    Sdetails["supplierlocation"] = sloc
    Sdetails["suppliedproducts"] = soty
    by = ObjectStorage.get_item(name, name + "hub")
    by = by.decode("UTF-8")
    data = json.loads(by)
    print(data)
    for x in data["listofhubs"]:
        if x["hubname"] == hub:
            print(x)
            nw = x
            by = ObjectStorage.get_item(x['ownername'], x['ownername'] + "hub")
            by = by.decode("UTF -8")
            by = json.loads(by)
            for t in by["listofhubs"]:
                if t["HubName"] == hub:
                    x = t
            x["SupplierDetails"].append(Sdetails)
            print(by)
            file = open(nw['ownername'] + "hub", "w")
            file.write(json.dumps(by))
            file.close()
            ObjectStorage.multi_part_upload(nw['ownername'], nw['ownername'] + "hub",
                                            os.path.abspath(nw['ownername'] + "hub"))
            print(data)
            os.remove(os.path.abspath(nw['ownername'] + "hub"))
            break
    f = open(name + "hub", "w")
    f.write(json.dumps(data))
    f.close()
    ObjectStorage.multi_part_upload(name, name + "hub", os.path.abspath(name + "hub"))
    print(data)
    os.remove(os.path.abspath(name + "hub"))
    return render_template("HubEntry.html", name=name)


@app.route("/productdetails/<name>", methods=["POST"])
def productdetails(name):
    hubname = request.form["fname"]
    print(hubname)
    by = ObjectStorage.get_item(name, name + "hub")
    print(by)
    b = by.decode("UTF-8")
    data = json.loads(b)
    senddata=""
    for x in data["listofhubs"]:
        if x["hubname"] == hubname:
            by=ObjectStorage.get_item(x["ownername"],x["ownername"]+"hub")
            by=by.decode("UTF -8")
            by=json.loads(by)
            for y in by["listofhubs"]:
                if y["HubName"] == hubname:
                    senddata = json.dumps(y["ProductDetails"])
                    break
            break

    return senddata


@app.route("/supplierdetails/<name>", methods=["POST"])
def supplierdetails(name):
    hubname = request.form["fname"]
    print(hubname)
    by = ObjectStorage.get_item(name, name + "hub")
    print(by)
    b = by.decode("UTF-8")
    data = json.loads(b)
    senddata = ""
    for x in data["listofhubs"]:
        if x["hubname"] == hubname:
            by = ObjectStorage.get_item(x["ownername"], x["ownername"] + "hub")
            by = by.decode("UTF -8")
            by = json.loads(by)
            for y in by["listofhubs"]:
                if y["HubName"] == hubname:
                    senddata = json.dumps(y["SupplierDetails"])
                    break
            break
    return senddata


@app.route("/changepassword/<name>")
def changepassword(name):
    print(name)
    return render_template("passwordchange.html", name=name)


@app.route("/passwordvalidate", methods=["POST"])
def validatepassword():
    password = request.form["pass"]
    username = request.form["name"]
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
            while result != False:
                if (result["USERNAME"] == username and result["PASSWORD"] == password):
                    otp[result["USERNAME"]] = TwoStepAuthenticator.generateOTP()
                    TwoStepAuthenticator.send_otp(result["MAILID"], otp[result["USERNAME"]])
                    return ""
                else:
                    result = ibm_db.fetch_both(stmt)
            return "incorrect password"

        except:
            return "incorrect password"
    except:
        return "something went wrong"


@app.route("/verifyotp", methods=["POST"])
def verifyotp():
    print("hii fro verifier of otp")
    mail = request.form["mail"]
    ot = request.form["otp"]
    print(mail)
    print(ot)
    if otp[mail] == ot:
        print("matched")
        return "otp matched"
    print("mismatch")
    return "otp mismatch"


@app.route("/psck", methods=["POST"])
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


@app.route("/passwordchange/<name>", methods=["POST"])
def changed(name):
    newpas = request.form["pass"]
    print(newpas)

    try:
        con = ibm_db.connect(
            "DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fzn32689;PWD=bPKXp7YkTR3uKK3a",
            '', '')
        qry1 = f"SELECT  * FROM FZN32689.REGISTRATION"
        stmt = ibm_db.exec_immediate(con, qry1)
        qry = ""
        result = ibm_db.fetch_both(stmt)
        username = ""
        mailid = ""
        phno = ""
        subuser = ""
        while result != False:
            if result["USERNAME"] == name:
                username = result['USERNAME']
                mailid = result['MAILID']
                phno = result['PHNO']
                subuser = result['SUBUSER']
                qry = f"INSERT INTO  FZN32689.REGISTRATION (USERNAME,MAILID,PHNO,PASSWORD,SUBUSER) VALUES('{username}','{mailid}','{phno}','{newpas}',0);"
                db = '"FZN32689"."REGISTRATION"  '
                un = '"USERNAME"'
                nm = "'bhawin'"
                qry2 = f"DELETE FROM          {db}         WHERE {un} = {nm};"

                stmt = ibm_db.exec_immediate(con, qry2)
                stmt = ibm_db.exec_immediate(con, qry)
                break
            else:
                result = ibm_db.fetch_both(stmt)

    except Exception as e:
        print(e)
        return "Something went wrong"
    return redirect("http://127.0.0.1:5002/profile/" + name)


@app.route("/removeproductdetails", methods=["POST"])
def removepd():
    hubname = request.form["hubname"]
    prname = request.form["prdname"]
    username = request.form["urname"]
    data = ObjectStorage.get_item(username, username + "hub")
    data = data.decode("UTF -8")
    print(data)
    data = json.loads(data)
    for x in data["listofhubs"]:
        if x["hubname"] == hubname:
            b = ObjectStorage.get_item(x["ownername"], x["ownername"] + "hub")
            print(b)
            b = b.decode("UTF -8")
            b = json.loads(b)
            for y in b["listofhubs"]:
                if y["HubName"] == hubname:
                    for z in y["ProductDetails"]:
                        if z["productname"] == prname:
                            y["ProductDetails"].remove(z)
                            break;
                    break
            file = open(x["ownername"] + "hub", "w")
            file.write(json.dumps(b))
            file.close()
            ObjectStorage.multi_part_upload(x["ownername"], x["ownername"] + "hub",
                                            os.path.abspath(x["ownername"] + "hub"))
            os.remove(os.path.abspath(x["ownername"] + "hub"))
            break

    print(data)
    file = open(username + "hub", "w")
    file.write(json.dumps(data))
    file.close()
    ObjectStorage.multi_part_upload(username, username + "hub", os.path.abspath(username + "hub"))
    os.remove(os.path.abspath(username + "hub"))

    return "Removed success fully refresh your page to see the changes"


@app.route("/removehub/<name>", methods=["POST"])
def removeHub(name):
    hubname = request.form["hub"]
    data = ObjectStorage.get_item(name, name + "hub")
    data = data.decode("UTF -8")
    print(data)
    data = json.loads(data)
    for x in data["listofhubs"]:
        if x["hubname"] == hubname:
            b=ObjectStorage.get_item(x["ownername"],x["ownername"]+"hub")
            print(b)
            b=b.decode("UTF -8")
            b=json.loads(b)
            for y in b["listofhubs"]:
                if y["HubName"] == hubname:
                    b["listofhubs"].remove(y)
                    break
            file = open(x["ownername"] + "hub", "w")
            file.write(json.dumps(b))
            file.close()
            ObjectStorage.multi_part_upload(x["ownername"],x["ownername"] + "hub", os.path.abspath(x["ownername"] + "hub"))
            os.remove(os.path.abspath(x["ownername"]+ "hub"))
            break
    file = open(name + "hub", "w")
    file.write(json.dumps(data))
    file.close()
    ObjectStorage.multi_part_upload(name, name + "hub", os.path.abspath(name + "hub"))
    os.remove(os.path.abspath(name + "hub"))
    return "Removed " + hubname + "successfully reload your page to see the changes"


@app.route("/removesupplier/<name>", methods=["POST"])
def removeSupplier(name):
    supname = request.form["sname"]
    hubname = request.form["hname"]
    data = ObjectStorage.get_item(name, name + "hub")
    data = data.decode("UTF -8")
    data = json.loads(data)
    for x in data["listofhubs"]:
            if x["hubname"] == hubname:
                b = ObjectStorage.get_item(x["ownername"], x["ownername"] + "hub")
                print(b)
                b = b.decode("UTF -8")
                b = json.loads(b)
                for y in b["listofhubs"]:
                    if y["HubName"] == hubname:
                        for z in y["SupplierDetails"]:
                            if z["suppliername"] == supname:
                                y["SupplierDetails"].remove(z)
                                break;
                        break
                file = open(x["ownername"] + "hub", "w")
                file.write(json.dumps(b))
                file.close()
                ObjectStorage.multi_part_upload(x["ownername"], x["ownername"] + "hub",
                                                os.path.abspath(x["ownername"] + "hub"))
                os.remove(os.path.abspath(x["ownername"] + "hub"))
                break

            break
    file = open(name + "hub", "w")
    file.write(json.dumps(data))
    file.close()
    ObjectStorage.multi_part_upload(name, name + "hub", os.path.abspath(name + "hub"))
    os.remove(os.path.abspath(name + "hub"))
    return "Removed " + supname + "successfully reload your page to see the changes"


@app.route("/changepname/<name>", methods=["POST"])
def changePname(name):
    pname = request.form["prdname"]
    olpname = request.form["olpname"]
    hname = request.form["hubname"]
    print(pname)
    print(olpname)
    print(hname)
    data = ObjectStorage.get_item(name, name + "hub")
    data = data.decode("UTF -8")
    data = json.loads(data)
    for x in data["listofhubs"]:
        if x["hubname"] == hname:
            b = ObjectStorage.get_item(x["ownername"], x["ownername"] + "hub")
            print(b)
            b = b.decode("UTF -8")
            b = json.loads(b)
            for y in b["listofhubs"]:
                if y["HubName"] == hname:
                    for z in y["ProductDetails"]:
                        if z["productname"] == olpname:
                            z["productname"] = pname
                            break;
                    break
            file = open(x["ownername"] + "hub", "w")
            file.write(json.dumps(b))
            file.close()
            ObjectStorage.multi_part_upload(x["ownername"], x["ownername"] + "hub",
                                            os.path.abspath(x["ownername"] + "hub"))
            os.remove(os.path.abspath(x["ownername"] + "hub"))
            break

    return "changed successfully"


@app.route("/changesname/<name>", methods=["POST"])
def changeSname(name):
    sname = request.form["prdname"]
    olpname = request.form["olpname"]
    hname = request.form["hubname"]
    print(sname)
    print(olpname)
    print(hname)
    data = ObjectStorage.get_item(name, name + "hub")
    data = data.decode("UTF -8")
    data = json.loads(data)
    for x in data["listofhubs"]:
        if x["hubname"] == hname:
            b = ObjectStorage.get_item(x["ownername"], x["ownername"] + "hub")
            print(b)
            b = b.decode("UTF -8")
            b = json.loads(b)
            for y in b["listofhubs"]:
                if y["HubName"] == hname:
                    for z in y["ProductDetails"]:
                       if z["productname"] == olpname:
                           z["suppliername"] = sname
                           break;
                    break
            file = open(x["ownername"] + "hub", "w")
            file.write(json.dumps(b))
            file.close()
            ObjectStorage.multi_part_upload(x["ownername"], x["ownername"] + "hub",
                                            os.path.abspath(x["ownername"] + "hub"))
            os.remove(os.path.abspath(x["ownername"] + "hub"))

            break
    return "changed successfully"


@app.route("/addpricedetails/<name>", methods=["POST"])
def addpricedetails(name):
    sname = request.form["prdname"]
    olpname = request.form["olpname"]
    hname = request.form["hubname"]
    price = request.form["price"]
    sprice = request.form["sprice"]
    date = request.form["date"]
    qty = request.form["qty"]
    print(sname)
    print(olpname)
    print(hname)
    data = ObjectStorage.get_item(name, name + "hub")
    data = data.decode("UTF -8")
    data = json.loads(data)
    pricedetails["productprice"] = price
    pricedetails["sellingprice"] = sprice
    pricedetails["date"] = date
    pricedetails["qty"] = qty
    for x in data["listofhubs"]:
        if x["hubname"] == hname:
            b = ObjectStorage.get_item(x["ownername"], x["ownername"] + "hub")
            print(b)
            b = b.decode("UTF -8")
            b = json.loads(b)
            for x in b["listofhubs"]:
                if x["HubName"] == hname:
                    for y in x["ProductDetails"]:
                        if y["productname"] == olpname:
                            y["pricedetails"].append(pricedetails)
                            print(pricedetails)
                            file = open(x["ownername"] + "hub", "w")
                            file.write(json.dumps(data))
                            file.close()
                            ObjectStorage.multi_part_upload(x["ownername"],x["ownername"] + "hub", os.path.abspath(x["ownername"] + "hub"))
                            os.remove(os.path.abspath(x["ownername"]+ "hub"))
                            break
            break
    return "Added successfully"


@app.route("/addsalesdetails/<name>", methods=["POST"])
def addsalesdetails(name):
    sname = request.form["prdname"]
    olpname = request.form["olpname"]
    hname = request.form["hubname"]
    date = request.form["date"]
    qty = request.form["qty"]

    data = ObjectStorage.get_item(name, name + "hub")
    data = data.decode("UTF -8")
    data = json.loads(data)
    sales["saledqty"] = qty
    sales["saleddate"] = date
    for x in data["listofhubs"]:
        if x["HubName"] == hname:
            for y in x["ProductDetails"]:
                if y["productname"] == olpname:
                    if y["productname"] == olpname and y["suppliername"] == sname:
                        dy = 0;
                        mnt = 0;
                        yr = 0;
                        qt = ""
                        zin = ""
                        for z in y["pricedetails"]:
                            dt = z["date"]
                            dt = dt.split("-")
                            print(dt)
                            print(type(int(dt[0])))
                            if int(dt[0]) > yr:
                                yr = int(dt[0])
                                qt = z["qty"]
                                zin = z
                            if mnt < int(dt[1]):
                                mnt = int(dt[1])
                                qt = z["qty"]
                                zin = z
                            if dy < int(dt[2]):
                                dy = int(dt[2])
                                qt = z["qty"]
                                zin = z
                        text = ""
                        numbers = ""
                        text1 = ""
                        numbers1 = ""
                        for i in zin["qty"]:
                            if (i.isdigit()):
                                numbers += i
                            else:
                                text += i
                        for i in qty:
                            if (i.isdigit()):
                                numbers1 += i
                            else:
                                text1 += i
                        zin["qty"] = str(abs(int(numbers1) - int(numbers))) + text1
                        newqty = abs(int(numbers1) - int(numbers))
                        by = ObjectStorage.get_item(name, name + "settings")
                        by = by.decode("UTF -8")
                        by = json.loads(by)
                        num = ""
                        if text != "":
                            for i in by["productalertkl"]:
                                if (i.isdigit()):
                                    num += i
                        else:
                            num = by["productalertcnt"]
                        print(num)
                        if newqty <= int(num):
                            by = ObjectStorage.get_item(name, name + "profile")
                            by = by.decode("UTF -8")
                            by = json.loads(by)
                            print(by)
                            TwoStepAuthenticator.message(by["mailId"], "Low stock ",
                                                         "Losw stock  make an order to meet out the demand product name= " + olpname + "quantity left=" + str(
                                                             newqty) + text1)

                    y["salesdetails"].append(sales)
                    print(pricedetails)
                    file = open(name + "hub", "w")
                    file.write(json.dumps(data))
                    file.close()
                    ObjectStorage.multi_part_upload(name, name + "hub", os.path.abspath(name + "hub"))
                    os.remove(os.path.abspath(name + "hub"))
                    break
            break
    return "Added successfully"


@app.route("/changesdname/<name>", methods=["POST"])
def changeSdname(name):
    pname = request.form["prdname"]
    olpname = request.form["olpname"]
    hname = request.form["hubname"]
    print(pname)
    print(olpname)
    print(hname)
    data = ObjectStorage.get_item(name, name + "hub")
    data = data.decode("UTF -8")
    data = json.loads(data)
    for x in data["listofhubs"]:
        if x["HubName"] == hname:
            for y in x["SupplierDetails"]:
                if y["suppliername"] == olpname:
                    y["suppliername"] = pname
                    file = open(name + "hub", "w")
                    file.write(json.dumps(data))
                    file.close()
                    ObjectStorage.multi_part_upload(name, name + "hub", os.path.abspath(name + "hub"))
                    os.remove(os.path.abspath(name + "hub"))
                    break
            break
    return "changed successfully"


@app.route("/changesdlocation/<name>", methods=["POST"])
def changeSdlocation(name):
    pname = request.form["prdname"]
    olpname = request.form["olpname"]
    hname = request.form["hubname"]
    print(pname)
    print(olpname)
    print(hname)
    data = ObjectStorage.get_item(name, name + "hub")
    data = data.decode("UTF -8")
    data = json.loads(data)
    for x in data["listofhubs"]:
        if x["HubName"] == hname:
            for y in x["SupplierDetails"]:
                if y["suppliername"] == olpname:
                    y["supplierlocation"] = pname
                    file = open(name + "hub", "w")
                    file.write(json.dumps(data))
                    file.close()
                    ObjectStorage.multi_part_upload(name, name + "hub", os.path.abspath(name + "hub"))
                    os.remove(os.path.abspath(name + "hub"))
                    break
            break
    return "changed successfully"


@app.route("/changesdqty/<name>", methods=["POST"])
def changeSdqty(name):
    pname = request.form["prdname"]
    olpname = request.form["olpname"]
    hname = request.form["hubname"]
    print(pname)
    print(olpname)
    print(hname)
    data = ObjectStorage.get_item(name, name + "hub")
    data = data.decode("UTF -8")
    data = json.loads(data)
    for x in data["listofhubs"]:
        if x["HubName"] == hname:
            for y in x["SupplierDetails"]:
                if y["suppliername"] == olpname:
                    y["suppliedproducts"] = pname
                    file = open(name + "hub", "w")
                    file.write(json.dumps(data))
                    file.close()
                    ObjectStorage.multi_part_upload(name, name + "hub", os.path.abspath(name + "hub"))
                    os.remove(os.path.abspath(name + "hub"))
                    break
            break
    return "changed successfully"
@app.route("/settings/<name>",methods=["POST"])
def settings(name):
    hr=request.form["hr"]
    pr=request.form["pr"]
    kl = request.form["kl"]
    cnt = request.form["cnt"]
    Settings["productalertkl"]=kl
    Settings["productalertcnt"]=str(cnt)
    Settings["productranking"]=pr
    Settings["hubranking"]=hr
    file=open(name+"settings","w")
    file.write(json.dumps(Settings))
    file.close()
    ObjectStorage.multi_part_upload(name,name+"settings",os.path.abspath(name+"settings"))
    os.remove(os.path.abspath(name+"settings"))


if __name__ == "__main__":
    app.run(port=5012, debug=True)




