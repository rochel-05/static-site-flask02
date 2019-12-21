from flask import flash, redirect, render_template, request, session, url_for
from flask_paginate import Pagination, get_page_args
import subprocess
from sqlalchemy.orm import sessionmaker
from table import *
from invetigate_RF import *

app = Flask(__name__)
engine = create_engine('sqlite:///usersDb.db', echo=True)

@app.route('/')
@app.route('/home/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return render_template('login.php')
    else:
        return render_template('index.php')

@app.route('/login/', methods=['POST'])
def login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route('/logout/')
def logout():
    session['logged_in'] = False
    return home()

@app.route('/detection/')
def detection():
    return render_template('detection.php')

def get_results(offset=0, per_page=10):
    duree, result = investigate_crash()
    return result[offset: offset + per_page], result, duree

@app.route('/crashDetection/', methods=["GET", "POST"])
def crash_detection():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination_users, result, duree = get_results(offset=offset, per_page=per_page)
    total = len(result)
    print('total : ', total)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    frame = request.form.get('frame')
    if request.method == 'GET' and frame:
        return redirect(url_for('recognizePlate', frame=frame))
    return render_template('detection_result.php',
                           results=pagination_users,
                           duration=duree,
                           users=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)

@app.route('/accuracy/')
def accuracy_test():
    return render_template('accuracy.php')

@app.route('/performance/', methods=["GET", "POST"])
def performance():
    return render_template('accuracy.php')

@app.route("/videoBtn/", methods=["GET", "POST"])
def findVideo():
    return render_template('detection.php')

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    return render_template('detection.php')

@app.route('/video/', methods=['GET', 'POST'])
def videos():
    return render_template('detection.php')

@app.route('/lpr/')
def lpr():
    return render_template('lpr.php')

@app.route('/recognizePlate/', methods=['GET', 'POST'])
def recognizePlate():
    return render_template('lpr.php')

@app.route('/alert/')
def alert():
    return render_template('alert.php')

@app.route('/emergency/', methods=['GET', 'POST'])
def emergency():
    return render_template('alert.php')

@app.route('/urgence/', methods=['GET', 'POST'])
def urgence():
    try:
        subprocess.call(r'C:\WINDOWS\system32\cmd.exe /C "C:\Users\ASUS\AppData\Local\CounterPath\X-Lite\Current\X-Lite.exe"')
    except:
        subprocess.call(r'C:\WINDOWS\system32\cmd.exe /C "C:\Users\ASUS\AppData\Local\CounterPath\X-Lite\Current\X-Lite.exe"')
    finally:
        subprocess.call(r'C:\WINDOWS\system32\cmd.exe /C "C:\Users\ASUS\AppData\Local\CounterPath\X-Lite\Current\X-Lite.exe"')
    return render_template('alert.php')

@app.errorhandler(404)
@app.errorhandler(401)
@app.errorhandler(500)
def page_not_found(error):
    return render_template('error.php', code=error.code)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)