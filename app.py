
# importing Flask module as this will be used to  create a flask web server
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy #SQLALchemy will make it easy to develop an SQL database and help create RBAC for the app
from flask_login import UserMixin, LoginManager #Provides user session management; logging in/out and authetnication
from flask_wtf import FlaskForm #Flask_form will create forms and  handle validation
from wtforms import StringField, PasswordField, SubmitField #will create fields for forms in web app and represent HTML code for web app
from wtforms.validators import InputRequired, Length, ValidationError #Will validate forms
from werkzeug.security import generate_password_hash
from flask_login import login_user
from werkzeug.security import check_password_hash
from flask import flash, redirect, url_for
#Login Manager will manage user logins
#Flask web application will be represented by app.py; __name__ means the current file (which is app.py)
app = Flask(__name__)

#app.rout() is stating what URL should trigger the function titled home() for the web application
@app.route('/')
def home():  # put application's code here
    return 'Hello World!'

#This is the main driver function, which will run the app sever and enable the Flask web app to run on port 5000
#__name__== ' main ' is checking if the web server is being ran directly on the file or if its indirectly ran/ imported
# app.py is running the web serverdirectly therefore == __main__
if __name__ == '__main__':
    app.run(port=5000)




#SQLite is a database engine; storing data for application
# Initialize SQLAlchemy with Flask application instance; configuring web app to use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' # the right most value is location of SQLite dabatase which flask app will use to store information
#Configuring location of SQLite datbase, its relative the location given so its in the same directoy, the datbase
db = SQLAlchemy(app) #create database instance by creating an instance of SQLAlchemy with flask application represented by 'app' argument



#Creating a User class for database, giving attributes such as an id, username, and password
#Starting out with fundamentals and will modify database schema as needed;i.e; RBAC; patients,doctors,etc
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # an int value which acts as a unique identifer for a user objectt/record in the table primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True) #Username for user can be a max of 100 chars long and username can't be taken
    password = db.Column(db.String(100)) #password can be a max of 100 char, *Will implement salting and hashing* in plaintext currently






# Initialize Flask-Login
login_manager = LoginManager() # login_managerObject will manage user sessions for app
login_manager.login_view = 'login' #this is telling login_manager to ensure user is redirected to 'login' webpage to login
login_manager.init_app(app) #Initializing loginmanager, connecting to flask web app



@login_manager.user_loader #This is calling Flask-Login to lookup a user from connected database
#The argument for the function is user_id, which is user ID string from database
def load_user(user_id):
    # since the user_id is just the primary key of our user table,
    # use it in the query for the user
    return User.query.get(int(user_id)) #It is querying the database to find a User object with the user_id given in the argument
#User.query.get is specific SQLAlchemy syntax to get an object by its primary keyl user_id
#It will either return 'None' or the user object
#It is getting converted to an int, as the database is expecting primary_key to be an integer








#Class for Registeration Form
#Each field 'username,password,submit is presented by an html field; Stringield creates an <input type="test>
#Password field function will create a <input type="password"> html field
#Submit Field creates a submit button field

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=80)])
    submit = SubmitField("Register")
    #validate_username, function
    def validate_username(self, username):
        #This line is stating if there is an existing 'User' object in the database to set it to exist_user_usnerame
        existing_user_username = User.query.filter_by(username=username.data).first()
        #Python has a special object called 'None'; so existing_user_username will either be 'None' or a user object
        #So if existing_user_username does exist, then raise a ValidationError
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")


#app.route for URL '/register' for app; which will have HTTP get and POST for registering account
#Trigger the register() function whenever /register is accessed
#Decorator tells flask that the function immediately following shoild run if there is an HTTP GET or POST request for /register
@app.route('/register', methods=['GET', 'POST'])
def register():
    #Intiialize a new registration form
    form = RegisterForm()
    #Function will see if POST request has been made for form and if all form fields are valid
    #The function will either turn True or False
    #If the POST request has been made and fields are valid; create the user and add it to the database
    #also return a string "New user has been created" as the HTTP response
    if form.validate_on_submit():
        #hashed_password; ensure password isn't stored in plain text
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user) #adding user to current databa session
        db.session.commit() #commits; writes session to database; adds user to database
        flash('Congratulations, you are now a registered user!') #flash message for successful registration
        return redirect(url_for('login')) #will redirect user after successful registration to login route

    return render_template('register.html', title='Register', form=form) #if form was invalid, render register webpage along with render the form



#Creating Login Form class, username,password and submission button
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=80)])
    submit = SubmitField("Login")





#Creating login URL route for app, will call login function everytime /login is accessed
@app.route('/login', methods=['GET', 'POST'])
def login():
    #creating Login Form
    form = LoginForm()
    #if form is validated, then create a user object by searching for a user with username in form data in database
    #Creating SQL query which will either return a 'User' or 'None'
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #If user was not found in database or if the password was not a match in the database
        if user is None or not check_password_hash(user.password, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        #If a user is found and password matched, a welcome message is flashed to user, stating their username
        flash('Welcome, {}!'.format(user.username))
        return redirect(url_for('index')) #redirect to index route
    #If a GET request is made to '/login' or if form validation fails then the login webpage with the form is rendered
    return render_template('login.html', title='Sign In', form=form)




#if user navigates to root of application ('/') or if they navigate to ('/index') then the index() will be called
@app.route('/')
@app.route('/index')
def index():
    #returns object of rendered html template and an argument of title as 'Home'
    return render_template('index.html', title='Home')


#Testing



