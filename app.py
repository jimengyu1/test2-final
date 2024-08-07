from flask import Flask, render_template, request
from pymysql import connections
import os
import random
import argparse

# Import the required libraries
import requests
from flask import send_from_directory

  


app = Flask(__name__)

DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "passwors"
DATABASE = os.environ.get("DATABASE") or "employees"
COLOR_FROM_ENV = os.environ.get('APP_COLOR') or "lime"
IMAGE_URL = os.environ.get("IMAGE_URL") or "Broken IMG"
GROUP_NAME = os.environ.get("GROUP_NAME")

DBPORT = os.environ.get("DBPORT")
if DBPORT is not None:
    try:
        DBPORT = int(DBPORT)
    except ValueError:
        print("Invalid value for DBPORT. Using default port.")
        DBPORT = 3306
else:
    DBPORT = 3306

# Create a connection to the MySQL database
db_conn = connections.Connection(
    host= DBHOST,
    port=DBPORT,
    user= DBUSER,
    password= DBPWD, 
    db= DATABASE
    
)
output = {}
table = 'employee';




# Define the path where you'll save the downloaded image
DOWNLOADS_PATH = "static/downloads"
if not os.path.exists(DOWNLOADS_PATH):
    os.makedirs(DOWNLOADS_PATH)
    
    
# Download the image from the S3 URL
# IMAGE_URL = "https://imagefinalproject.s3.amazonaws.com/backgroupimage.webp"
IMAGE_PATH = os.path.join(DOWNLOADS_PATH, "backgroupimage1.jpg")
response = requests.get(IMAGE_URL)
if response.status_code == 200:
    with open(IMAGE_PATH, "wb") as f:
        f.write(response.content)
    print("Image downloaded successfully.")
else:
    print("Failed to download image.")

# Define a variable for the image path
BACKGROUND_IMAGE_PATH = "/static/downloads/backgroupimage1.jpg"  
print(BACKGROUND_IMAGE_PATH)


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', background_image=BACKGROUND_IMAGE_PATH, GROUP_NAME=GROUP_NAME)

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', background_image=BACKGROUND_IMAGE_PATH, GROUP_NAME=GROUP_NAME)
    
@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

  
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        
        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('addempoutput.html', name=emp_name, background_image=BACKGROUND_IMAGE_PATH, GROUP_NAME=GROUP_NAME)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
     return render_template("getemp.html", background_image=BACKGROUND_IMAGE_PATH, GROUP_NAME=GROUP_NAME)


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()
        
        # Add No Employee found form
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"],  background_image=BACKGROUND_IMAGE_PATH, GROUP_NAME=GROUP_NAME)



app.run(host='0.0.0.0',port=81,debug=True)
