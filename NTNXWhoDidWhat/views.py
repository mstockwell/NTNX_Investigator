from NTNXWhoDidWhat import app
from WdWController import test_credentials, get_events_data
from flask import request, render_template, redirect, url_for, session


@app.route('/', methods=['GET', 'POST'])
def homepage():
    error = None
    if request.method == 'POST':
        ip_address = request.form['ip_address']
        username = request.form['username']
        password = request.form['password']
        try:
            status, cluster_info = test_credentials(username, password, ip_address)
            if status == 200:
                session["cluster_name"] = cluster_info.get('name')
                return redirect(url_for('querymainpage', cluster_name=session["cluster_name"]))
            else:
                return render_template("error.html", error=status)
        except Exception as e:
            return render_template("error.html", error=str(e))
    return render_template('homepage.html', error=error)


@app.route('/querymainpage', methods=['GET', 'POST'])
def querymainpage():
    error = None
    if request.method == 'POST':
        session["investigate_date"] = request.form['investigate_date']
        if session["investigate_date"] != "":
            try:
                session["unique_accounts"], events = get_events_data(session["investigate_date"])
                return render_template('results.html', cluster_name=session["cluster_name"],
                                       num_events=len(events),
                                       unique_accounts=session["unique_accounts"], events_list=events,
                                       investigate_date=session["investigate_date"])
            except Exception as e:
                return render_template("error.html", error=str(e))
        else:
            error = "You must enter a valid date to search"
            return render_template('querymainpage.html', cluster_name=session["cluster_name"], error=error)
    else:
        return render_template('querymainpage.html', cluster_name=session["cluster_name"], error=error)


@app.route('/results', methods=['GET', 'POST'])
def results():
    error = None
    if request.method == 'POST':
        try:
            session["unique_accounts"], events = get_events_data(session["investigate_date"])
        except Exception as e:
            return render_template("error.html", error=str(e))
        unique_account = request.form['account_id']
        unique_events = []
        if unique_account != "all_accounts":
            for event in events:
                if event[0] == unique_account:
                    unique_events.append(event)
        else:
            unique_events = events
        return render_template('results.html', cluster_name=session["cluster_name"], num_events=len(unique_events),
                               unique_accounts=session["unique_accounts"], events_list=unique_events,
                               investigate_date=session["investigate_date"])
    else:
        return render_template('querymainpage.html', cluster_name=session["cluster_name"], error=error)
