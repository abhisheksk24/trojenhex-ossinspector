# Importing essential libraries
from os import link
import string
from flask import Flask, render_template, request,jsonify
import requests
import requests.exceptions
import json
import datetime
from datetime import date as date_n
from collections import Counter


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
        avatar = str(tempusername["avatar_url"])


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
        lastupdated = str(output["updated_at"])[0:10]
        watchers = int(output["subscribers_count"])

        #License 
        templicense = (output["license"]) 
        if templicense is None:
            license1="None"
        else:
            license1 = str(templicense["name"])

        #Cntributions
        contributorsapi = urll+"/contributors"
        contributorsdata = requests.get(contributorsapi)
        contributorsdata2 = json.loads(contributorsdata.text)
        count = 0
        for i in range(0, len(contributorsdata2)):
            if "id" in contributorsdata2[i]:
                count = count+1
        

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

        #Days Since Repo Updated
        int_year_lup = int(str(lastupdated)[0:4])
        int_month_lup = int(str(lastupdated)[5:7])
        int_date_lup = int(str(lastupdated)[8:10])

        def number_of_days_lup(date_11, date_22):  
            return(date_22 - date_11).days 
       
        #Driver program  
        date_11 = date_n(int_year_lup, int_month_lup, int_date_lup)  
        date_22 = date_n(int_cur_year, int_cur_month, int_cur_date)

        repolastupdated = int(number_of_days_lup(date_11,date_22))+1

        def percentage(part, whole):
                return float(100 * float(part)/float(whole))

        #Stars Percentage
        stars_percentage = 0
        if (stars<1000):
            part = stars
            whole = 1000
            stars_percentage = int(percentage(part,whole))
        else :
            stars_percentage = 100

        #Forks Percentage
        forks_percentage = 0
        if (forks<350):
            part = forks
            whole = 350
            forks_percentage = float(percentage(part,whole))
        else :
            forks_percentage = 100

        #Issues Percentage (Negative Impact on score)
        issues_percentage = 0
        if (issues<50):
            part = issues
            whole = 200
            issues_percentage = -float(percentage(part,whole))
        else :
            issues_percentage = -30

        #Watchers Percentage
        watchers_percentage = 0
        if (watchers<25):
            part = watchers
            whole = 25
            watchers_percentage = float(percentage(part,whole))
        else :
            watchers_percentage = 100

        #Contributors Percentage
        contributors_percentage = 0
        if (count<15):
            part = count
            whole = 15
            contributors_percentage = float(percentage(part,whole))
        else :
            contributors_percentage = 100
        
        # license score
        license_percentage=0
        if license1=="None":
            license_percentage = -5
        else:
            license_percentage=80


        #Average Score
        sum_list = [stars_percentage,forks_percentage,issues_percentage,watchers_percentage,contributors_percentage,license_percentage]

        def Average(l): 
            avg = sum(l) / len(l) 
            return avg

        average = round(Average(sum_list),2)

        #Ratings
        if (average<70):
            rating = "Good"
            rating_color = "warning"

            if(average<50):
                rating = "Poor"
                rating_color = "danger"

                if(average<25):
                    rating = "Unsafe"
                    rating_color = "danger"

        else :
            rating = "Excellent"
            rating_color = "success"

              
        return render_template('result.html', ui_reponame = reponame, ui_username = username, ui_desc = description, 
        ui_stars = stars, 
        ui_forks = forks, 
        ui_issues = issues, 
        ui_language = language, 
        ui_follower = follower, 
        ui_repoage = age, 
        ui_contri = count, 
        ui_curdate = int_cur_year, 
        ui_license = license1, 
        ui_stars_percentage = stars_percentage, 
        ui_score = average ,
        ui_repolastupdated = repolastupdated, 
        ui_watchers = watchers,
        ui_avatar = avatar,
        ui_rating = rating,
        ui_rcolor = rating_color)


if __name__ == '__main__':
	app.run(debug=True)