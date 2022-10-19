from flask import Flask, render_template, url_for 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/signin")
def signin():
    return render_template('signin.html')

@app.route("/signup")
def signup():
    return render_template('signup.html') 

if __name__ == '__main__':
    app.run()       
