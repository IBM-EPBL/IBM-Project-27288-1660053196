from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3

#cur.execute("""CREATE TABLE signup(id INTEGER PRIMARY KEY AUTOINCREMENT ,mailid TEXT NOT NULL, username TEXT NOT NULL,phno TEXT ,password TEXT NOT NULL);""")
#cur.execute("INSERT INTO signup (mailid,username,phno,password) values('bj@gmail.com','bj','7402688321','123456');")
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        mailid = request.form['mail']
        password = request.form["pass"]
        con = sqlite3.connect("assignment.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM signup WHERE mailid='"+mailid+"'")
        res=cur.fetchone()
        if(len(res)>0):
         if(password==res[4]):
            con.commit()
            con.close()
            return render_template("home.html",name=res[2])
        else:
            return render_template("signup.html")
    else:
        return render_template("login.html")
@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'POST':
          con = sqlite3.connect("assignment.db")
          cur = con.cursor()
          mailid=request.form['mail']
          name=request.form['name']
          ph=request.form['ph']
          passw=request.form['pass']
          cur.execute("SELECT * FROM signup WHERE mailid='" + mailid + "'")
          if (len(cur.fetchall()) > 0):
                  return render_template("login.html")
          else:
              cur.execute(
                  "INSERT INTO signup (mailid,username,phno,password) values('"+mailid+"','"+name+"','"+ph+"','"+passw+"');")
              con.commit()
              con.close()
              return render_template("login.html")

          return render_template("signup.html")
    else:
        return render_template("signup.html")

if __name__ == "__main__":
    app.run()
