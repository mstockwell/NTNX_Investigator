from NTNXWhoDidWhat import app
from NTNXInvestigator import test_credentials, get_events_data
from flask import request, render_template, redirect,url_for


@app.route('/', methods=['GET', 'POST'])
def HomePage():
    error = None
    if request.method == 'POST':
        ip_address = request.form['ip_address']
        username = request.form['username']
        password = request.form['password']
        serverResponse = test_credentials(username, password,ip_address)
        if serverResponse.status_code==200:
            return redirect(url_for('querymainpage'))
        else:
            print "Nutant, we have a problem!"
    return render_template('homepage.html', error=error)


@app.route('/querymainpage', methods=['GET', 'POST'])
def querymainpage():
    error = None
    if request.method == 'POST':
        investigate_date = request.form['investigate_date']
        events = get_events_data(investigate_date)
        return render_template('results.html', num_events=len(events),events_list=events, investigate_date=investigate_date)
    return render_template('querymainpage.html', error=error)