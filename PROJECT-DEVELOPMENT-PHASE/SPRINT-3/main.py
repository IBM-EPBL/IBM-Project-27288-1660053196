from flask import Flask,render_template,request
import json
import PIL.Image as Image
import io
import os
import ObjectStorage

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
if __name__=="__main__":
    app.run(port=5012,debug=True)


