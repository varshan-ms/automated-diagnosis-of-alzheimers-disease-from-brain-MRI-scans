from flask import Flask, render_template, flash, request, session, send_file
from flask import render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
import mysql.connector
import sys

import pickle

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/Home")
def Home():
    return render_template('index.html')


@app.route("/DoctorLogin")
def DoctorLogin():
    return render_template('DoctorLogin.html')


@app.route("/NewDoctor")
def NewDoctor():
    return render_template('NewDoctor.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/Cancer")
def Cancer():
    return render_template('Cancer.html')


@app.route("/Diabetes")
def Diabetes():
    return render_template('Diabetes.html')


@app.route("/Heart")
def Heart():
    return render_template('Heart.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            return render_template('AdminHome.html', data=data)

        else:

            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()

    return render_template('AdminHome.html', data=data)

@app.route("/AdminUserInfo")
def AdminUserInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctortb ")
    data = cur.fetchall()

    return render_template('AdminUserInfo.html', data=data)


@app.route("/AdminAssignInfo")
def AdminAssignInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM drugtb ")
    data = cur.fetchall()

    return render_template('AdminAssignInfo.html', data=data)


@app.route("/DoctorUserInfo")
def DoctorUserInfo():
    dname = session['dname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName='" + dname + "' ")
    data = cur.fetchall()

    return render_template('DoctorUserInfo.html', data=data)


@app.route("/DoctorAssignInfo")
def DoctorAssignInfo():
    dname = session['dname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM drugtb where DoctorName='" + dname + "' ")
    data = cur.fetchall()

    return render_template('DoctorAssignInfo.html', data=data)


@app.route("/doclogin", methods=['GET', 'POST'])
def doclogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['dname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
        cursor = conn.cursor()
        cursor.execute("SELECT * from doctortb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            data1 = 'Username or Password is wrong'
            return render_template('goback.html', data=data1)


        else:
            print(data[0])
            session['uid'] = data[0]
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM doctortb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()

            return render_template('DoctorHome.html', data=data)


@app.route("/searchid")
def searchid():
    user = request.args.get('user')
    session['user'] = user
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
    cur = conn.cursor()
    cur.execute(
        "SELECT  *  FROM apptb where  username='" + str(user) + "'")
    data = cur.fetchall()
    print(data)

    return render_template('AdminAssign.html', data=data)


@app.route("/assigndrug", methods=['GET', 'POST'])
def assigndrug():
    if request.method == 'POST':
        uname = request.form['UserName']
        phone = request.form['Phone']
        email = request.form['Email']
        dname = session['dname']
        medi = request.form['Medicine']
        other = request.form['Other']
        file = request.files['file']
        file.save("static/upload/" + file.filename)
        Adate = request.form['Adate']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO  drugtb VALUES ('','" + uname + "','" + phone + "','" + email + "','" + dname + "','" + medi + "','" + other + "','" + file.filename + "','" + Adate + "')")
        conn.commit()
        conn.close()

        # return 'file register successfully'
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute("SELECT * FROM drugtb where DoctorName='" + dname + "' ")
        data = cur.fetchall()

    return render_template('DoctorAssignInfo.html', data=data)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        pnumber = request.form['phone']
        address = request.form['address']

        uname = request.form['uname']
        password = request.form['psw']
        loc = request.form['loc']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('" + name1 + "','" + gender1 + "','" + Age + "','" + email + "','" + pnumber + "','" + address + "','" + uname + "','" + password + "','" + loc + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'

    return render_template('UserLogin.html')


@app.route("/newdoctor", methods=['GET', 'POST'])
def newcoor():
    if request.method == 'POST':
        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        pnumber = request.form['phone']
        address = request.form['address']
        special = request.form['special']
        loc = request.form['loc']

        uname = request.form['uname']
        password = request.form['psw']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO doctortb VALUES ('" + name1 + "','" + gender1 + "','" + Age + "','" + email + "','" + pnumber + "','" + address + "','" + special + "','" + uname + "','" + password + "','" + loc + "')")
        conn.commit()
        conn.close()

    data1 = 'Record Saved'
    return render_template('goback.html', data=data1)


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            data1 = 'Username or Password is Incorrect!'
            return render_template('goback.html', data=data1)



        else:
            print(data[0])
            session['uid'] = data[0]
            session['loca'] = data[8]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()

            return render_template('UserHome.html', data=data)


@app.route("/ViewDoctor")
def ViewDoctor():
    return render_template('UserAppointment.html')


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        file.save('static/upload/Test.jpg')
        fname = 'static/upload/Test.jpg'

        import warnings
        warnings.filterwarnings('ignore')

        import tensorflow as tf
        import numpy as np
        import os
        from keras.preprocessing import image
        base_dir = 'Datas/train/'
        catgo = os.listdir(base_dir)
        print(catgo)

        classifierLoad = tf.keras.models.load_model('Vggmodel/model.h5')
        test_image = image.load_img('static/upload/Test.jpg', target_size=(100, 100))
        test_image = np.expand_dims(test_image, axis=0)
        result = classifierLoad.predict(test_image)
        print(result)
        ind = np.argmax(result)

        print(catgo[ind])

        if result[0][0] == 1:
            print("VeryMildDemented")
            out = "VeryMildDemented"

        elif result[0][1] == 1:
            print("MildDemented")
            out = "MildDemented"

        elif result[0][2] == 1:
            print("NonDemented")
            out = "NonDemented"

        if out == "NonDemented":
            print('Normal')
            return render_template('UserAppointment.html', pre=out)
        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
            cur = conn.cursor()
            cur.execute("SELECT * FROM doctortb ")
            data = cur.fetchall()
            session['out'] = out
            return render_template('UserAppointment.html', pre=out, data=data)


@app.route("/UserSearch", methods=['GET', 'POST'])
def UserSearch():
    if request.method == 'POST':
        special = request.form['special']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute("SELECT * FROM doctortb where Specialist='" + special + "'")
        data = cur.fetchall()

        return render_template('UserAppointment.html', data=data)


@app.route("/UserAppointment")
def UserAppointment():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM  apptb where UserName='" + uname + "' ")
    data = cur.fetchall()

    return render_template('UserAppointmentinfo.html', data=data)


@app.route("/UserAssignDrugInfo")
def UserAssignDrugInfo():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  drugtb where UserName='" + uname + "'  ")
    data = cur.fetchall()

    return render_template('UserAssignDrugInfo.html', data=data)


@app.route("/Appointment")
def Appointment():
    dusername = request.args.get('id')
    import datetime
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    uname = session['uname']
    dise = session['out']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM  doctortb where  UserNAme='" + dusername + "'")
    data = cursor.fetchone()

    if data:
        spec = data[6]

    else:

        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM regtb where  UserNAme='" + uname + "'")
    data = cursor.fetchone()

    if data:
        mobile = data[4]
        email = data[3]


    else:

        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO  apptb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + dusername + "','" + date + "','" + spec + "','"+ dise  +"')")
    conn.commit()
    conn.close()

    data1 = 'Record Saved'
    return render_template('goback.html', data=data1)


@app.route('/download')
def download():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM drugtb where  id = '" + str(id) + "'")
    data = cursor.fetchone()
    if data:
        filename = "static\\upload\\" + data[7]

        return send_file(filename, as_attachment=True)

    else:
        return 'Incorrect username / password !'


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        date = request.form['date']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2doctorapdbPy')
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute("SELECT * FROM assigntb where Lastdate='" + date + "'")
        data = cur.fetchall()

        return render_template('Notification.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
