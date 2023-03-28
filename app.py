import os
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pyshorteners

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

class URL(db.Model):
    __tablename__ = 'URLs'
    id = db.Column(db.Integer, primary_key = True)
    user_url = db.Column(db.String(100))
    short_url = db.Column(db.String(100))


    def __init__(self,user_url,short_url):
        self.user_url = user_url
        self.short_url= short_url


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/result',methods=['GET',"POST"])
def result():
    user_url = request.form['url']
    str = pyshorteners.Shortener()
    short_url = str.tinyurl.short(user_url)
    url = URL(user_url=user_url, short_url = short_url)
    db.session.add(url)
    db.session.commit()
    return render_template('home.html',short_url=short_url)


@app.route('/history', methods = ['GET','POST'])
def history():
    hist = URL.query.all()
    return render_template('history.html',hist = hist)



if __name__ == '__main__':
    app.run(debug=True)
