from flask import Flask,render_template
app=Flask(__name__)
@app.route("/")
def check():
    return render_template("check.html")

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5010,debug=True)