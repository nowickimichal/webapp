from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics
import numpy as np

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///formdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)

class Formdata(db.Model):
    __tablename__ = 'formdata'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    firstname = db.Column(db.String, nullable=False)
    email = db.Column(db.String) 
    age = db.Column(db.Integer)
    gender = db.Column(db.String) 
    weigth = db.Column(db.Integer)
    heigth = db.Column(db.Integer)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Integer)
    q6 = db.Column(db.Integer)
    q7 = db.Column(db.Integer)
    q8 = db.Column(db.Integer)
    q9 = db.Column(db.Integer)
    q10 = db.Column(db.Integer)
    q11 = db.Column(db.Integer)
    q12 = db.Column(db.Integer)
    

    def __init__(self, firstname, gender, email, age, weigth, heigth, q1, q2, q3, q4, q5, q6, q7, q8 , q9 , q10 , q11 , q12):
        self.firstname = firstname
        self.gender = gender
        self.email = email
        self.age = age
        self.weigth = weigth
        self.heigth = heigth
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.q5 = q5
        self.q6 = q6
        self.q7 = q7
        self.q8 = q8
        self.q9 = q9
        self.q10 = q10
        self.q11 = q11
        self.q12 = q12
       
    
 
db.create_all()


@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/form")
def show_form():
    return render_template('form.html')

@app.route("/raw")
def show_raw():
    fd = db.session.query(Formdata).all()
    return render_template('raw.html', formdata=fd)


@app.route("/result")
def show_result():
    fd_list = db.session.query(Formdata).all()

    # Some simple statistics for sample questions
    heigth = []
    weigth = []
    gender = []
    

    for el in fd_list:
        heigth.append(int(el.heigth))
        weigth.append(int(el.weigth))
        gender.append(str(el.gender))
        
#        q3.append(int(el.q3))
#        q4.append(int(el.q4))
#        q5.append(int(el.q5))
#        q6.append(int(el.q6))
#        q7.append(int(el.q7))
#        q8.append(int(el.q8))
#        q9.append(int(el.q9))
#        q10.append(int(el.q2))
#        q11.append(int(el.q1))
#        q12.append(int(el.q2))
    
    BMI=np.zeros(len(heigth))
    sum_BMI_m=0
    sum_BMI_w=0
    sum_BMIX=0
    w=0
    m=0
    for i in range (0,len(heigth)):
        BMI[i]=weigth[i]/((heigth[i]/100)*((heigth[i]/100)))
    if len(BMI)>0:
        mean_BMI= statistics.mean(BMI)
    else:
        mean_BMI=0
    
    for i in range (0,len(heigth)):
        if gender[i]=='M':
            sum_BMI_m=sum_BMI_m+BMI[i]
            m=m+1
        elif gender[i]=='K':
            sum_BMI_w=sum_BMI_w+BMI[i]
            w=w+1
        else:
            sum_BMIX=BMI[i]
    if w>0:
        mean_BMI_w=sum_BMI_w/w
    else:
        mean_BMI_w=0
    if m>0:
        mean_BMI_m=sum_BMI_m/m
    else:
        mean_BMI_m=0
        
        
        
    
            
  
    
    
    

    
    


    # Prepare data for google charts
    data = [['Średnie BMI', (mean_BMI)], ['Średnie BMI Kobiety', (mean_BMI_w)], ['Średnie BMI Męższczyźni', mean_BMI_m]] 

    return render_template('result.html', data=data)


@app.route("/save", methods=['POST'])
def save():
    # Get data from FORM
    firstname = request.form['firstname']
    gender = request.form['gender']
    email = request.form['email']
    age = request.form['age']
    weigth = request.form['weigth']
    heigth = request.form['heigth']
    q1 = request.form['q1']
    q2 = request.form['q2']
    q3 = request.form['q3']
    q4 = request.form['q4']
    q5 = request.form['q5']
    q6 = request.form['q6']
    q7 = request.form['q7']
    q8 = request.form['q8']
    q9 = request.form['q9']
    q10 = request.form['q10']
    q11 = request.form['q11']
    q12 = request.form['q12']

    # Save the data
    fd = Formdata(firstname, gender, email, age, weigth, heigth, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12)
    db.session.add(fd)
    db.session.commit()
 
    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()
 