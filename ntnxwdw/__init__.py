from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = '023aM47zz19Sx873yew9321Pl8746'

from ntnxwdw import els_views
