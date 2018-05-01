import random
from flask import Flask, render_template, redirect, url_for,request,flash
from flask_bootstrap import Bootstrap
from flask_wtf import Form 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin,AdminIndexView
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

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15))
	email = db.Column(db.String(50))
	password = db.Column(db.String(80))
	isadmin = db.Column(db.Integer)
	category=db.Column(db.String(30))
	sub_category=db.Column(db.String(30))
	question1=db.Column(db.String(30))
	question2=db.Column(db.String(30))
	question3=db.Column(db.String(30))
	question4=db.Column(db.String(30))
	question5=db.Column(db.String(30))
	isquiz_complete=db.Column(db.Integer)
	quiz_score=db.Column(db.Integer)
	role=db.Column(db.Boolean,default=False)



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
	question_number=db.Column(db.Integer)
	question     = db.Column(db.String(500))
	option_1     = db.Column(db.String(50))
	option_2     = db.Column(db.String(50))
	option_3     = db.Column(db.String(50))
	option_4     = db.Column(db.String(50))
	answer    	 = db.Column(db.String(10))
	qtype=db.Column(db.Integer)

class MyModelView(ModelView):
	def is_accessible(self):
		if current_user.is_anonymous is not True:
			if current_user.role == True:
				return True
			return False
		return False

class MyAdminViewIndex(AdminIndexView):
	def is_accessible(self):
		if current_user.is_anonymous is not True:
			if current_user.role == True:
				return True
			return False
		return False
		return current_user.is_authenticated


pop={'sports':{'football','cricket','hockey'},'general':{'static','current_affairs','mix-bag'},'culture':{'drama','musicanddance','folk'},'history':{'ancient','medieval','modern'}}

@app.route('/populate')
def populate():
	x=[1,2,3,4,12,13,14,23,24,34,123,124,134,234,1234]
	counter=1
	for i in pop:
		for j in pop[i]:
			for k in range(1,6):
				p="this is question "+str(k) 
				temp=quizdata(answer=random.choice(x),question=p,category=i,sub_category=j,question_number=k,option_1="this is option 1",option_2="this is option 2",option_3="this is option 3",option_4="this is option 4")
				db.session.add(temp)
				db.session.commit()
				counter+=1

admin.add_view(MyModelView(User,db.session))
admin.add_view(MyModelView(quizdata,db.session))


@app.route('/evaluate/<cat>/<subcat>',methods=['GET', 'POST'])
def evaluate(cat,subcat):
	temp=User.query.filter_by(username=current_user.username,category=cat,sub_category=subcat).first()
	quiz_tempi=quizdata.query.filter_by(category=cat,sub_category=subcat).all()
	skore=0
	for i in range(1,6):
		quiz_temp=quizdata.query.filter_by(category=cat,sub_category=subcat,question_number=i).first()
		if(''.join(temp.question1.split(","))==quiz_temp.answer):
			skore+=1
		if(''.join(temp.question2.split(","))==quiz_temp.answer):
			skore+=1
		if(''.join(temp.question3.split(","))==quiz_temp.answer):
			skore+=1
		if(''.join(temp.question4.split(","))==quiz_temp.answer):
			skore+=1
		if(''.join(temp.question5.split(","))==quiz_temp.answer):
			skore+=1
	
		
	
	temp.isquiz_complete=1
	temp.quiz_score=skore%6
	db.session.commit()

	lisk={'questions':[],'answers':[],'ganswers':[]}
	
	for i in range(1,6):
		q=quizdata.query.filter_by(category=cat,sub_category=subcat,question_number=i).first().question
		a=quizdata.query.filter_by(category=cat,sub_category=subcat,question_number=i).first().answer
		ga=User.query.filter_by(username=current_user.username,category=cat,sub_category=subcat).first()
		lisk['questions'].append(q)
		lisk['answers'].append(a)
		if(i==1):
			lisk['ganswers'].append(''.join(ga.question1.split(",")))
		if(i==2):
			lisk['ganswers'].append(''.join(ga.question2.split(",")))
		if(i==3):
			lisk['ganswers'].append(''.join(ga.question3.split(",")))
		if(i==4):
			lisk['ganswers'].append(''.join(ga.question4.split(",")))
		if(i==5):
			lisk['ganswers'].append(''.join(ga.question5.split(",")))
		
	for i in lisk['ganswers']:
		print(i)
	return render_template('kachra.html',lisk=lisk,ga=ga)



@app.route('/process/<cat>/<subcat>/<int:num>/<is_continue>',methods=['GET', 'POST'])
def process(cat,subcat,num,is_continue):
	x=",".join(request.form.getlist("check"))
	temp=User.query.filter_by(username=current_user.username,category=cat,sub_category=subcat).first()
	if(num==1):
		temp.question1=x
	if(num==2):

		temp.question2=x
	if(num==3):

		temp.question3=x
	if(num==4):
		
		temp.question4=x
	if(num==5):
		
		temp.question5=x
	db.session.commit()		
	thread = quizdata.query.filter_by(category=cat,sub_category=subcat).paginate(per_page=1, page=num, error_out=True)
	data=quizdata.query.filter_by(category=cat,sub_category=subcat).all()
	f=len(quizdata.query.filter_by(category=cat,sub_category=subcat,question_number=num).first().answer)
	
	return render_template('contact.html',f=f,quark=x,page_num=num,thread=thread,cat=cat,subcat=subcat,data=data,is_continue=is_continue)

@app.route('/quiz/<cat>/<subcat>/<int:page_num>/<is_continue>')
@login_required
def contact(page_num,cat,subcat,is_continue):
	data=quizdata.query.filter_by(category=cat,sub_category=subcat).all()
	f=len(quizdata.query.filter_by(category=cat,sub_category=subcat,question_number=page_num).first().answer)
	thread = quizdata.query.filter_by(category=cat,sub_category=subcat).paginate(per_page=1, page=page_num, error_out=True)
	if(User.query.filter_by(username=current_user.username,category=cat,sub_category=subcat).first().isquiz_complete==0 and is_continue=="yes"):
		tempo=User.query.filter_by(username=current_user.username,category=cat,sub_category=subcat).first()
		if(page_num==1):
			quark=tempo.question1
		if(page_num==2 ):
			quark=tempo.question2
		if(page_num==3 ):
			quark=tempo.question3
		if(page_num==4 ):
			quark=tempo.question4
		if(page_num==5 ):
			quark=tempo.question5
		count=0
		for i in data:
			count=count+1

		return render_template('contact.html',f=f,quark=quark,page_num=page_num,thread=thread,cat=cat,subcat=subcat,data=data,is_continue=is_continue)

	if(User.query.filter_by(username=current_user.username,category=cat,sub_category=subcat).first().isquiz_complete==0 and is_continue=="no"):
		temp=User.query.filter_by(username=current_user.username,category=cat,sub_category=subcat).first()
		temp.question1=""
		temp.question2=""
		temp.question3=""
		temp.question4=""
		temp.question5=""
		temp.isquiz_complete=0
		temp.quiz_score=0
		db.session.commit()
		tempo=User.query.filter_by(username=current_user.username,category=cat,sub_category=subcat).first()
		
		data=quizdata.query.filter_by(category=cat,sub_category=subcat).all()
		thread = quizdata.query.filter_by(category=cat,sub_category=subcat).paginate(per_page=1, page=page_num, error_out=True)
			
		tempo=User.query.filter_by(username=current_user.username,category=cat,sub_category=subcat).first()
		if(page_num==1):
			quark=tempo.question1
		if(page_num==2 ):
			quark=tempo.question2
		if(page_num==3 ):
			quark=tempo.question3
		if(page_num==4 ):
			quark=tempo.question4
		if(page_num==5 ):
			quark=tempo.question5
		is_continue="yes"
		return render_template('contact.html',f=f,quark=quark,page_num=page_num,thread=thread,cat=cat,subcat=subcat,data=data,is_continue=is_continue)
		
	else:
		return '<h1>you have already given the quiz</h1>'

@app.route('/performance/<cat>/<subcat>')
@login_required
def performance(cat,subcat):
	y=User.query.filter_by(username=current_user.username,category=cat,sub_category=subcat).first()	
	x=User.query.filter_by(category=cat,sub_category=subcat).all()
	lis=[]
	t=0
	for i in x:
		lis.append([i.username,i.quiz_score,i.isquiz_complete,0])

	lis.sort(key=lambda x:x[1],reverse=True)
	'''t=0
	for i in x:
		if(i==y):
			store2=t
		t+=1'''
	tank=0
	rank=1
	for i in lis:
		i[3]=rank
		if(i[0]==y.username):
			tank=rank
		rank+=1
	
	return render_template('performance.html',global_topper=lis[0][1],global_rank=tank,obj=y)

@app.route('/')
def index():
	return render_template('home1.html')

cats={'sports':['hockey','cricket','football'],'culture':['drama','music and dance','folk'],'social-science':['civics','geo','his']}

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registerpage()
    flag=0
    flagi=0
    if form.validate_on_submit():
        secret = generate_password_hash(form.password.data, method='sha256')
        for i in User.query.all():
        	if(i.username==form.username.data):
        		flag=1
        	if(i.email==form.email.data):
        		flagi=1
        if(flag!=1 and flagi!=1):
        	for i in pop:
        		for j in pop[i]:
        			new_user=User(question1="",question2="",question3="",question4="",question5="",username=form.username.data,email=form.email.data, password=secret,isadmin=0,category=i,sub_category=j,isquiz_complete=0,quiz_score=0)
        			db.session.add(new_user)
        			db.session.commit()
        	return render_template('new.html')

    return render_template('register.html', form=form,flag=flag,flagi=flagi)
        	

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginpage()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data,isadmin=0).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)

@app.route('/loginadmin', methods=['GET', 'POST'])
def loginadmin():
    form = loginpage()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data,isadmin=1).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect('http://127.0.0.1:5000/admin')

        return '<h1>Invalid username or password</h1>'

    return render_template('login2.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dash.html', name=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('http://127.0.0.1:5000/')

@app.route('/leaderboard/<cat>/<subcat>')
@login_required
def leaderboard(cat,subcat):
	x=User.query.filter_by(category=cat,sub_category=subcat).all()	
	lis=[]
	for i in x:
		lis.append([i.username,i.quiz_score,i.isquiz_complete,0])
	lis.sort(key=lambda x:x[1],reverse=True)

	rank=1

	for i in lis:
		i[3]=rank
		rank+=1
	return render_template('leaderboard.html',lis=lis)

if __name__ == '__main__':
	db.init_app(app)
	db.create_all()
	app.run(debug=True)

