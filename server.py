#import libraries
import numpy as np
from flask import Flask, render_template,request,redirect
import pickle

#Initialize the flask App
app = Flask(__name__)

@app.route('/myapp', methods=['GET','POST'])
def myapp():
   return render_template("app.html")

#To use the predict button in our web-app
@app.route('/predict',methods=['POST'])
def predict():
    model = pickle.load(open('mymodel.pickle', 'rb'))

    # For rendering results on HTML GUI
    prg = request.form['preg']
    glc = request.form['g1']
    bp = request.form['bp']
    skt = request.form['sk']
    ins = request.form['ins']
    bmi = request.form['BMI']
    dpf = request.form['pf']
    age = request.form['Age']

    prg = int(prg)
    glc = int(glc)
    bp = int(bp)
    skt = int(skt)
    ins = int(ins)
    bmi = float(bmi)
    dpf = float(dpf)
    age = int(age)
#   int_features = [int(x) for x in request.form.values()]
    final_features = np.array([(prg, glc, bp, skt, ins, bmi, dpf, age)])
    sc=pickle.load(open('scaler.sav','rb'))
    sc.fit(final_features)
    final_features=sc.transform(final_features)

    prediction = model.predict(final_features)
    if prediction[0]==0:
        p="The patient has no diabetes"
    else:
        p="The patient has diabetes"
    #output = round(prediction[0], 2)
    return render_template("app.html", prediction_text='Diabetics report :{}'.format(p))

if __name__ == "__main__":
    app.run(debug=True)