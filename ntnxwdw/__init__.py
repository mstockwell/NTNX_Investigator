from flask import Flask
import requests.packages.urllib3

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = '023aM47zz19Sx873yew9321Pl8746'
requests.packages.urllib3.disable_warnings()
from ntnxwdw import els_controller
