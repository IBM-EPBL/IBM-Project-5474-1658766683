import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask,render_template,request
from twilio.rest import Client
import cv2
import numpy as np
from playsound import playsound
from flask import Flask, render_template

app=Flask(__name__)

model=load_model("ffd_model.h5")
  
@app.route('/')
def index():
    return render_template("index.html")
text=''
@app.route('/predict',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        f=request.files['image']
        filepath=os.path.join('static/',f.filename)
        f.save(filepath)
        img=image.load_img(filepath,target_size=(128,128))
        x=image.img_to_array(img)
        x = np.expand_dims(x,axis=0)
        pred = model.predict(x)
        y = int(pred[0][0])
        if(pred==1):
            account_sid = os.environ['TWILIO_ACCOUNT_SID']
            auth_token = os.environ['TWILIO_AUTH_TOKEN']
            client = Client(account_sid,auth_token)
            msg = client.messages.create(
                body="Fire Detected! Get to safety immediately!!!!",
                from_=os.environ['TWILIO_PHONE_NUMBER'],
                to=os.environ['PHONE_NUMBER']
                )
            print(msg.sid)
            text='FIRE DETECTED!!! SMS SENT!!'
            playsound('alert.mp3')
        else:
            text='NO FIRE'
    return text

if __name__=='__main__':
    app.run(debug=False)
