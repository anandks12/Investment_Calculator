from math import exp
from flask import Flask,render_template, request,redirect,url_for
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
oauth=OAuth(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///calculation.db'
db=SQLAlchemy(app)

app.config['GOOGLE_CLIENT_ID'] ="1033385120324-5lvtl1unkj1fk4sd32d5fd0vpk17di99.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "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"
app.config['SECRET_KEY']  = "THIS SHOULD BE SECRET"
google = oauth.register(
    name = 'google',
    client_id = app.config["GOOGLE_CLIENT_ID"],
    client_secret = app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  
    client_kwargs = {'scope': 'openid email profile'},
)
class Calculate(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    salary=db.Column(db.Integer,nullable=False)
    savings=db.Column(db.Integer,nullable=False)
    vehicle=db.Column(db.Integer,nullable=False)
    rent=db.Column(db.Integer,nullable=False)
    children=db.Column(db.Integer,nullable=False)
    other=db.Column(db.Integer,nullable=False)
    exp=db.Column(db.Integer,nullable=False)
    credit=db.Column(db.Integer,nullable=False)
    debit=db.Column(db.Integer,nullable=False)
    def __repr__(self):
        return 'Calculate'+str(self.id)
@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        return redirect('/cal')
    else:
        return render_template('index.html')
@app.route('/cal',methods=['GET','POST'])
def cal():
    if request.method=='POST':
        form=request.form
        cal_a=form['salary']
        cal_b=form['savings']
        cal_c=form['vehicle']
        cal_d=form['rent']
        cal_e=form['children']
        cal_f=form['other']
        cal_g=int(cal_a)+int(cal_b)
        cal_h=int(cal_c)+int(cal_d)+int(cal_e)+int(cal_f)
        cal_exp=int(cal_a)+int(cal_b)-int(cal_c)-int(cal_d)-int(cal_e)-int(cal_f)
        calculate=Calculate(
            salary=cal_a,
            savings=cal_b,
            vehicle=cal_c,
            rent=cal_d,
            children=cal_e,
            other=cal_f,
            debit=cal_g,
            credit=cal_h,
            exp=cal_exp
        )
        db.session.add(calculate)
        db.session.commit()
        return render_template('invest.html',exp1=calculate)
    else:
        calculate=Calculate.query.order_by(Calculate.salary).all()
        return render_template('cal.html')
@app.route('/invest',methods=['POSTS','GET'])            
def invest():
    if request.method=='GET':
        return render_template('invest.html')
@app.route('/login')        
def login():
    return render_template('login.html')
@app.route('/login/google')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)
@app.route('/login/google/authorize')
def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    print(f"\n{resp}\n")
    return redirect('/cal')
@app.route('/logout')    
def logout():
    return redirect('/')
if __name__ ==  "__main__"  :
    app.run(debug=False,host='0.0.0.0')    
