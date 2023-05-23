
# importing Flask module as this will be used to  create a flask web server
from flask import Flask
from flask_sqlalchemy import SQLAlchemy #SQLALchemy will make it easy to develop an SQL database and help create RBAC for the app
from flask_login import UserMixin, LoginManager #Provides user session management; logging in/out and authetnication
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


#Testing



