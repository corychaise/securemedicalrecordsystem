
# importing Flask module as this will be used to  create a flask web server
from flask import Flask


#Flask web application will be represented by app.py; __name__ means the current file (which is app.py)
app = Flask(__name__)

#app.rout() is stating what URL should trigger the function titled home() for the web application
@app.route('/')
def home():  # put application's code here
    return 'Hello World!'

#This is the main driver function, which will run the app sever and enable the Flask web app to run on port 5000
#__name__ refers to current file
if __name__ == '__main__':
    app.run(port=5000)


#Testing