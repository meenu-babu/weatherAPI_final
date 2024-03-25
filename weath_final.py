from flask import Flask,render_template,request, redirect, url_for,flash
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from dotenv import load_dotenv
import os
import secrets
load_dotenv()

app=Flask(__name__)


app.secret_key = secrets.token_hex(16)  # Generates a 32-character hexadecimal string

#app.secret_key = 'ITS A SECRET KEY'
database_uri = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI']=database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


#print("Database URI from environment variable:", database_uri)



db = SQLAlchemy(app)

class weath(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   lattitude = db.Column(db.Float, index=True)
   longitude = db.Column(db.Float)
   temperature = db.Column(db.Float)
   __table_args__ = (
      Index('ix_lattitude', 'lattitude', unique=False),
   )


#def __init__(self, lattitude,longitude):
 #  self.lattitude = lattitude
  # self.longitude = longitude
def create_tables():
    with app.app_context():
        db.create_all()
        #if 'weath' not in db.metadata.tables:
         #   print("Error: Table 'weath' was not created successfully.")
        #else:
         #   print("Table 'weath' created successfully.")

api_key=os.getenv('api_key')
@app.route("/",methods=['GET','POST'])
def WeatherInputPage():
    temperatureData = "" 
    if request.method=='POST' and 'lattitude'in request.form:
        lat=float(request.form.get('lattitude'))
        lon=float(request.form.get('longitude'))
        cached_weather = weath.query.filter_by(lattitude=lat, longitude=lon).first()
        if cached_weather:
            temperatureData = cached_weather.temperature
            flash('Temperature data retrieved from cache')
        else:
            url=f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
            response = requests.get(url)
            data = response.json()
            temperatureData=f"{data['main']['temp']}"
            weathdata=weath(lattitude=lat, longitude=lon,temperature=temperatureData)
            db.session.add(weathdata)
            db.session.commit()
            flash('Record was successfully added')

    return render_template("weath.html", temperatureData=temperatureData)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)