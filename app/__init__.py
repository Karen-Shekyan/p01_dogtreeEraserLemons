from flask import Flask, render_template, session
import requests, os

app = Flask(__name__)
secret_key = os.urandom(32)

@app.route('/')
def login():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

