import socket
from flask import Flask, render_template
app = Flask(__name__)
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
print("Your Computer Name is:"+hostname)
print("Your Computer IP Address is:"+IPAddr)

@app.route('/')
def hello():
    return "Your Computer IP Address is:"+IPAddr