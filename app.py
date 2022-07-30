# Importing essential libraries
from os import link
import string
from flask import Flask, render_template, request,jsonify
import requests
import requests.exceptions
import json
import datetime
from datetime import date as date_n


app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/inspect', methods=['POST'])
def inspect():
    temp_array = list()
    
    if request.method == 'POST':
            
        link1 = str(request.form['repo_link'])

        temp_array = temp_array + [link]
        urll = "https://api.github.com/repos/{}".format(link1)

        savedinfo = requests.get(urll)
        output = json.loads(savedinfo.text)

        tempusername = (output["owner"])
        username = str(tempusername["login"])


        userdetails = "https://api.github.com/users/{}".format(username)
        saveduserinfo = requests.get(userdetails)
        useroutput = json.loads(saveduserinfo.text)

        #From Repo
        reponame = str(output["name"])
        forks = int(output["forks"])
        stars = int(output["stargazers_count"])
        language = str(output["language"])
        issues = int(output["open_issues"])
        description = str(output["description"])
        creation_date = str(output["created_at"])[0:10]
        contributions = str(output["subscribers_count"])

        #License 
        templicense = (output["license"])
        license1 = str(templicense["name"])
        

        #From User Profile
        follower = str(useroutput["followers"])

        #Coverting to Int
        int_year = int(str(creation_date)[0:4])
        int_month = int(str(creation_date)[5:7])
        int_date = int(str(creation_date)[8:10])

        #Repo Age Calculator
        current_date =  datetime.date.today()
        int_cur_year = int(str(current_date)[0:4])
        int_cur_month = int(str(current_date)[5:7])
        int_cur_date = int(str(current_date)[8:10])

        def number_of_days(date_1, date_2):  
            return(date_2 - date_1).days  
       
        #Driver program  
        date_1 = date_n(int_year, int_month, int_date)  
        date_2 = date_n(int_cur_year, int_cur_month, int_cur_date)

        age = int(number_of_days(date_1,date_2))
        
              
        return render_template('result.html', ui_reponame = reponame, ui_username = username, ui_desc = description, ui_stars = stars, ui_forks = forks, 
        ui_issues = issues, ui_language = language, ui_follower = follower, ui_repoage = age, ui_contri = contributions, ui_curdate = int_cur_year, ui_license = license1)


if __name__ == '__main__':
	app.run(debug=True)