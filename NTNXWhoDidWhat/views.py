from NTNXWhoDidWhat import app
from WdWController import test_credentials, get_events_data
from flask import request, render_template, redirect, url_for


@app.route('/', methods=['GET', 'POST'])
def HomePage():
    error = None
    if request.method == 'POST':
        ip_address = request.form['ip_address']
        username = request.form['username']
        password = request.form['password']
        status, cluster_info = test_credentials(username, password, ip_address)
        if status == 200:
            return redirect(url_for('querymainpage', cluster_name=cluster_info.get('name')))
        else:
            print "Nutant, we have a problem!"
    return render_template('homepage.html', error=error)


@app.route('/querymainpage', methods=['GET', 'POST'])
def querymainpage():
    error = None
    if request.method == 'POST':
        investigate_date = request.form['investigate_date']
        events = get_events_data(investigate_date)
        return render_template('results.html', num_events=len(events), events_list=events,
                               investigate_date=investigate_date)
    else:
        cluster_name = request.args.get('cluster_name')
        return render_template('querymainpage.html', cluster_name=cluster_name, error=error)
