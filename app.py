import numpy as np
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import pickle

app = Flask(__name__)

rf = pickle.load(open('cardio.pkl','rb')) # Load pickle object


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cardiotest'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("home.html") 

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        fullname = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO cardiotest.cardiouserinfo (FullName, email, password)VALUES (%s,%s,%s)",(fullname, email, password,))
        mysql.connection.commit()
        session['name'] = fullname,
        session['email'] = email
        return redirect(url_for('login'))
        
@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM cardiotest.cardiouserinfo WHERE email=%s",(email,))
        user = cursor.fetchone()
        if user is not None:
            if password == user["password"]:
                session['name'] = user['FullName'] 
                session['email'] = user['email']
                return redirect(url_for('cardioTest'))

            else:
                return "Error Password or username doesn't match"
        else:
            return "Null"
            
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")


####### Cardio Test ######

@app.route('/cardioTest')
def cardioTest():
    return render_template('cardio.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method=='POST':
       intput_features = [float(x) for x in request.form.values()]
       final_features = [np.array(intput_features)]
       prediction = rf.predict(final_features)
      
       if prediction == 1:
           output = "You are affected by Cardiovascular Disease"
       if prediction == 0:
           output="You are not affected by Cardiovascular Disease"
       

    return render_template('predict.html', outcome = output)



if __name__ == '__main__':
    app.secret_key = "^A%DJkljjklAJU^JJ"
    app.run(debug=True)
