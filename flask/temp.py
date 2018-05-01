from flask import Flask, render_template, redirect, url_for,request,flash
from flask_bootstrap import Bootstrap
from flask_wtf import Form 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from wtforms import validators, ValidationError
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SECRET_KEY'] = 'randomshithaikoipehchannalebhenchod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
admin=Admin(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
'''above line function??'''

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

admin.add_view(ModelView(User,db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class loginpage(Form):
    username = StringField('username', validators=[InputRequired(), Length(min=2, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
class registerpage(Form):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=2, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])



class quizdata(UserMixin,db.Model):
	id = db.Column(db.Integer, primary_key=True)
	category     = db.Column(db.String(30))
	sub_category = db.Column(db.String(30))
	question     = db.Column(db.String(500))
	option_1     = db.Column(db.String(50))
	option_2     = db.Column(db.String(50))
	option_3     = db.Column(db.String(50))
	option_4     = db.Column(db.String(50))
	answer       = db.Column(db.Integer)

admin.add_view(ModelView(quizdata,db.session))


'''class ContactForm(Form):
   options = RadioField('options', choices = [('1',''),('2',''),('3',''),(4,'')])
   submit = SubmitField("Send")'''


#@app.route('/quiz', methods = ['GET', 'POST'])
#def contact():
	#x=quizdata.query.filter_by(category="sports",sub_category="cricket")
	#i=x.first()
	#return render_template('contact.html',list=[i.option_1,i.option_2,i.option_3,i.option_4],question=i.question)

'''@app.route('/quiz/<int:page_num>')
def threads(page_num):
	threads = quizdata.query.filter_by(category="sports",sub_category="cricket").paginate(per_page=1, page=page_num, error_out=True)
	return render_template('index.html',threads=threads)'''

@app.route('/record_answer',methods=['GET', 'POST'])
def record_answer():
	return '<h>heloo</h>'


@app.route('/')
def index():
	#return render_template('home.html')
	#test=quizdata(category="history",sub_category="mughal",question="was babur gay?",option_1="yes",option_2="no",option_3="cant say",option_4="hell yeah",answer="13")
	
	# for i in range (1,10):
	# test=quizdata()
	#db.session.add(test)
	#db.session.commit()
	return render_template('home1.html',contact="contact")
	#return '<h2>hey bitch</h2>'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registerpage()
    flag=0
    flagi=0
    if form.validate_on_submit():
        secret = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=secret)
        for i in User.query.all():
        	if(i.username==new_user.username):
        		flag=1
        	if(i.email==new_user.email):
        		flagi=1
        if(flag!=1 and flagi!=1):
        	db.session.add(new_user)
        	db.session.commit()
        	return '<h1>welcome to the world of quizzing!</h1>'

    return render_template('register.html', form=form,flag=flag,flagi=flagi)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginpage()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



if __name__ == '__main__':
	db.init_app(app)
	db.create_all()
	app.run(debug=True)
