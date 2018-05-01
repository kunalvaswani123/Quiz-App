													QUIZIT
											online quizzing app

INSTRUCTIONS:

a.ABOUT

1)Download the complete app folder which includes database,templates and the control code.
3.3)user will have two types of questions that is multiple choice correct and single choice correct2)The control 
code has been written in python 3 and the web framework used is Flask with Jinja-2 for rendering templates.
3)For the purpose of linking and manipulating database through python control code, flask SQLAlchemy has been used.
4)Simple deployment of ap4 is possible by running the python file "app.py".5

b.PREREQUISITES:

1)Must have python 3.2 installed.
2)Must have SQLITE3 insed.
3)latest version of flask must be installed.
4)Following modules/libraries should be installed for using the app :
	3.1)Flask SQLAlchemy
	3.2)Flask Wtforms,Wtforms Validators
	3.3)Flask werkzeug security
	3.4)Flask modelview
	3.5)Flask_admin.contrib.sqla
	3.6)Flask login,admin,user
	3.7)pip3 latest version 
5)All above can be installed using command line command: "sudo-pip3 install <--->"
6)basic knowledge of using sqlite3 for dropping and building tables accordingly as the app allows user to customise his quiz categories from the code itself(for users who want to learn from the app):

	5.1)sqlite3 data.db
	5.2)drop quizdata


c.FUNCTIONALITIES AND WEBSITE-INTERACTION:

1)separate login for user and admin
2)ADMIN:
	2.1)can view cumulative records of any user and his performance.
	2.2)can control quizzes and the questions included in the quizzes.
3)USER:
	3.1)option of 4 different and broad categories of quizzes.
	3.2)each category has 3 sub-categories laced with 5 questions each.
	3.3)user will have two types of questions that is multiple choice correct and single choice correct
	3.4)user can see his performance by ranks on the leaderboards which are individually sorted for each category an sub category.
	3.5)user can see also see his quantitative analysis of performances based on an option which allows him to view all his performances till now.
	3.6)user can pause his quiz and leave anytime, if at all quiz is left unfinished due to power-cut or any other reason then he has option to resume his quiz or altogether start a new one.
	3.7)user can analyse his quizzes using piecharts taken directly from google analytics

d.Starting the App:

1)Do python3 app.py to run the app on your machine

e. Command Line Setup

1) Installing Modules on Command Line:

	a) sudo pip3 install flask-sqlalchemy

	b) sudo pip3 install flask-wtf

	c) sudo pip3 install werkzeug-security

	d) sudo pip3 install flask-admin

	e) sudo pip3 install flask-login

	f) sudo pip3 install wtfforms

	g) sudo pip3 install flask-bootstrap

2) Manipulating Database

	a) sqlite3 data.db

	b) drop table user;

	c) drop table quizdata;