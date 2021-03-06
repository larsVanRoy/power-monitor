from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required

from User import User
from Persistence import Persistence

import glob

app = Flask(__name__)
app.config.from_object("Config.Config")

login_manager = LoginManager()
login_manager.init_app(app)

User = User()
Persistence = Persistence()


@login_manager.user_loader
def load_user(user_id):
    session['id'] = user_id
    return User.get(user_id)


@app.route('/')
def main():
    if 'id' in session:
        Persistence.set_user(User.get(session['id']))
    return render_template("main.html")


@app.route('/past_week')
def display_past_week():
    user = User.get(session['id'])

    temp = glob.glob('static/plots/week_plot_el*')
    if len(temp) != 0:
        el_week = temp[0].split("/", maxsplit=1)[1]
    else:
        el_week = ''

    temp = glob.glob('static/plots/week_plot_g*')
    if len(temp) != 0:
        g_week = temp[0].split("/", maxsplit=1)[1]
    else:
        g_week = ''

    temp = glob.glob('static/plots/week_plot_s0*')
    if len(temp) != 0:
        s_week = temp[0].split("/", maxsplit=1)[1]
    else:
        s_week = ''

    print(el_week)
    print(g_week)

    return render_template("past_week.html", El=user.track_el, g=user.track_g, S0=user.track_s0,
                           el_week=url_for('static', filename=el_week).replace("%5C", "/"),
                           g_week=url_for('static', filename=g_week).replace("%5C", "/"),
                           s_week=url_for('static', filename=s_week).replace("%5C", "/"))


@app.route('/past_month')
def display_past_month():
    user = User.get(session['id'])

    temp = glob.glob('static/plots/month_plot_el*')
    if len(temp) != 0:
        el_month = temp[0].split("/", maxsplit=1)[1]
    else:
        el_month = ''

    temp = glob.glob('static/plots/month_plot_g*')
    if len(temp) != 0:
        g_month = temp[0].split("/", maxsplit=1)[1]
    else:
        g_month = ''

    temp = glob.glob('static/plots/month_plot_s0*')
    if len(temp) != 0:
        s_month = temp[0].split("/", maxsplit=1)[1]
    else:
        s_month = ''

    return render_template("past_month.html", El=user.track_el, g=user.track_g, S0=user.track_s0,
                           el_month=url_for('static', filename=el_month).replace("%5C", "/"),
                           g_month=url_for('static', filename=g_month).replace("%5C", "/"),
                           s_month=url_for('static', filename=s_month).replace("%5C", "/"))


@app.route('/past_year')
def display_past_year():
    user = User.get(session['id'])

    temp = glob.glob('static/plots/year_plot_el*')
    if len(temp) != 0:
        el_year = temp[0].split("/", maxsplit=1)[1]
    else:
        el_year = ''

    temp = glob.glob('static/plots/year_plot_g*')
    if len(temp) != 0:
        g_year = temp[0].split("/", maxsplit=1)[1]
    else:
        g_year = ''

    temp = glob.glob('static/plots/year_plot_s0*')
    if len(temp) != 0:
        s_year = temp[0].split("/", maxsplit=1)[1]
    else:
        s_year = ''

    return render_template("past_year.html", El=user.track_el, g=user.track_g, S0=user.track_s0,
                           el_year=url_for('static', filename=el_year).replace("%5C", "/"),
                           g_year=url_for('static', filename=g_year).replace("%5C", "/"),
                           s_year=url_for('static', filename=s_year).replace("%5C", "/"))


@app.route('/statistics', methods=['GET'])
def display_statistics():
    queries = Persistence.get_statistics()

    return render_template("statistics.html", queries=queries)


@app.route('/add_query', methods=['POST'])
def add_query():
    query_name = request.form.get('query name')
    query = request.form.get('query')

    Persistence.add_query(query_name, query)

    flash("Added query")
    return redirect(url_for('display_statistics'))


@app.route('/update_query', methods=['POST'])
def update_query():
    new_name = request.form.get('query name')
    new_query = request.form.get('query')

    old_name = request.form.get('orig query name')
    old_query = request.form.get('orig query')

    if old_name != new_name:
        Persistence.update_query_name(old_name, new_name)

    if old_query != new_query:
        Persistence.update_query_query(new_name, new_query)

    flash('Updated query')
    return redirect(url_for('display_statistics'))


@login_required
@app.route('/settings', methods=['GET'])
def settings():
    user = User.get(session['id'])

    temp = user.user_start.__str__().split("-")
    if temp[0] != 'None':
        start = temp[1] + '/' + temp[2] + '/' + temp[0]
    else:
        start = ""

    if user.track_el:
        track_el = "checked"
    else:
        track_el = ""

    if user.track_g:
        track_g = "checked"
    else:
        track_g = ""

    if user.track_s0:
        track_s0 = "checked"
    else:
        track_s0 = ""

    return render_template("settings.html", ip=user.user_ip, kwh_cost=user.user_kwh_price, gas_cost=user.user_gas_price,
                           start=start, track_el=track_el, track_g=track_g, track_s0=track_s0)


@login_required
@app.route('/settings', methods=['POST'])
def set_settings():
    ip = request.form.get('ip')
    start_date = request.form.get('start-date')
    track_el = request.form.get('enable_electricity')
    kwhcost = request.form.get('kwhcost')
    track_g = request.form.get('enable_gas')
    gascost = request.form.get('gascost')
    track_s0 = request.form.get('enable_s0')

    User.update_settings(ip, start_date, track_el, track_g, track_s0, kwhcost, gascost)

    flash("Settings have been updated!")
    return redirect(url_for('main'))


@login_required
@app.route('/update', methods=['POST'])
def update_database():
    Persistence.update(session['id'])

    flash("Database has been updated!")
    return redirect(url_for('main'))


@app.route('/login', methods=['GET'])
def render_login():
    return render_template("login.html")


@app.route("/login", methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.validate_login(username, password)
    if user is not None:
        login_user(user, remember=True)
        flash('Logged in successfully.')

        return redirect(url_for('main'))
    else:
        flash('Incorrect username or password, please try again.')

        return redirect(url_for('login'))


@app.route("/logout")
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run()
