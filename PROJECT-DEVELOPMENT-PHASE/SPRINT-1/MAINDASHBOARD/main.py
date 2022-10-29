from flask import Flask,render_template

import ibm_db

app = Flask(__name__)

@app.route("/dashboard/<name>")
def dashboard(name):
   return render_template("MainBoard.html",name=name)
@app.route("/profile/<name>")
def profile(name):
    return  render_template("profile.html",name=name)
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
if __name__=="__main__":
    app.run(port=5002,debug=True)


