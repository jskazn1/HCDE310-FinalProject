from flask import Flask
from flask import render_template
import os

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 8080, debug = True)