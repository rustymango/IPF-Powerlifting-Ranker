from __future__ import print_function
from cgitb import html
from django.shortcuts import render
from numpy import double
from collections import defaultdict
import pip._vendor.requests
import requests
import re
import numpy as np
from bson import ObjectId

#pandas
import pandas as pd
#beautiful soup parser
from bs4 import BeautifulSoup
#selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
#NoSQL db (mongoDB)
from pymongo import MongoClient

# Front-end inputs

# Hard coded user inputs
equipment = "raw"
weight = 160 
gender = "woman"
if gender == "man":
    gender = "men"
    #need way to automatically categorize
    if weight > 145 and weight <= 163:
        weight_class = "ipf74"
    elif weight > 163 and weight <= 183:
        weight_class = "ipf83"
        pass
else:
    #automatic categorization needed here too
    gender = "women"
    if weight > 138 and weight <= 152:
        weight_class = "ipf69"
    elif weight > 152 and weight <= 168:
        weight_class = "ipf76"
        pass
age = 21
#automatic categorization pls
if age > 20 and age <= 23:
    age = "20-23"
elif age > 23 and age <= 34:
    age = "24-34"
    pass
category = "by-total"

user_squat = 335
user_bench = 285
user_deadlift = 435
user_total = user_squat + user_bench + user_deadlift

# Selenium required as website uses API

# ser = Service("D:/Usuario/Desktop/chrome_driver/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(f'https://www.openpowerlifting.org/rankings/\
{equipment}/{weight_class}/{gender}/{age}/{category}')
driver.implicitly_wait(15)

squats = [user_squat]
benches = [user_bench]
deadlifts = [user_deadlift]

def grab_lift_data():

    # Retrieve lift data
    # does not need to be run once all data stored in database

    i = 0

    squat_data = driver.find_elements(By.CLASS_NAME, "squat")
    bench_data = driver.find_elements(By.CLASS_NAME, "bench")
    deadlift_data = driver.find_elements(By.CLASS_NAME, "deadlift")

    for squat in squat_data:
        squats.append(float(squat.text))
    for bench in bench_data:
        benches.append(float(bench.text))
    for deadlift in deadlift_data:
        deadlifts.append(float(deadlift.text))
    driver.execute_script("arguments[0].scrollIntoView(true);", squat_data[-1])
    time.sleep(2)

    while i <= 90:
        squat_data = driver.find_elements(By.CLASS_NAME, "squat")
        bench_data = driver.find_elements(By.CLASS_NAME, "bench")
        deadlift_data = driver.find_elements(By.CLASS_NAME, "deadlift")
        temp_squats = []
        temp_benches = []
        temp_deadlifts = []

        for squat in squat_data:
            if len(squat.text.strip()) > 0: 
                temp_squats.append(float(squat.text))
            else:
                temp_squats = temp_squats
        for bench in bench_data:
            if len(bench.text.strip()) > 0:
                temp_benches.append(float(bench.text))
            else:
                temp_benches = temp_benches
        for deadlift in deadlift_data:
            if len(deadlift.text.strip()) > 0:
                temp_deadlifts.append(float(deadlift.text))
            else:
                temp_deadlifts = temp_deadlifts

        driver.execute_script("arguments[0].scrollIntoView(true);", squat_data[-1])
        time.sleep(2)

        temp_squats[0:7] = []
        squats.extend(temp_squats)
        temp_benches[0:7] = []
        benches.extend(temp_benches)
        temp_deadlifts[0:7] = []
        deadlifts.extend(temp_deadlifts)

        i = i + 1

grab_lift_data()

# Insert data into MongoDB
# Only needs to be run once to store in DB, do not run otherwise

client = MongoClient()
client = MongoClient("localhost", 27017)

db = client.PowerliftingDB

# Store parsed data in db
def store_data():
    squats_dict = {"weight_class": weight_class, "lift": "squat"}
    squats_dict["squats"] = squats
    print(squats_dict)
    benches_dict = {"weight_class": weight_class, "lift": "bench"}
    benches_dict["benches"] = benches
    print(benches_dict)
    deadlifts_dict = {"weight_class": weight_class, "lift": "deadlift"}
    deadlifts_dict["deadlifts"] = deadlifts
    print(deadlifts_dict)

    if gender == "men":
        if age == "20-23":
            db.MenJunior.insert_one(squats_dict)
            db.MenJunior.insert_one(benches_dict)
            db.MenJunior.insert_one(deadlifts_dict)
        if age == "24-34":
            db.MenSenior.insert_one(squats_dict)
            db.MenSenior.insert_one(benches_dict)
            db.MenSenior.insert_one(deadlifts_dict)
    else:
        if age == "20-23":
            db.WomenJunior.insert_one(squats_dict)
            db.WomenJunior.insert_one(benches_dict)
            db.WomenJunior.insert_one(deadlifts_dict)
        if age == "24-34":
            db.WomenSenior.insert_one(squats_dict)
            db.WomenSenior.insert_one(benches_dict)
            db.WomenSenior.insert_one(deadlifts_dict)
    return

store_data()

# Query db
if gender == "men":
    if age == "20-23":
        database_id = "MenJunior"
    else:
        database_id = "MenSenior"
else:
    if age == "20-23":
        database_id = "WomenJunior"
    else:
        database_id = "WomenSenior"

def query_lift_db():
    
    global squats, benches, deadlifts

    lift_data = db.get_collection(database_id)
    squat_cursor = lift_data.find({"weight_class": weight_class, "lift": "squat"})
    bench_cursor = lift_data.find({"weight_class": weight_class, "lift": "bench"})
    deadlift_cursor = lift_data.find({"weight_class": weight_class, "lift": "deadlift"})

    for lift in squat_cursor:
        squats = lift["squats"]
        # print(squats)
    for lift in bench_cursor:
        benches = lift["benches"]
        # print(benches)
    for lift in deadlift_cursor:
        deadlifts = lift["deadlifts"]
        # print(deadlifts)

# query_lift_db()

# Calculate rank of user

squat_df = pd.DataFrame(squats)
bench_df = pd.DataFrame(benches)
deadlift_df = pd.DataFrame(deadlifts)

squat_rank = squat_df.lt(user_squat).sum()/len(squat_df)*100
bench_rank = bench_df.lt(user_bench).sum()/len(bench_df)*100
deadlift_rank = deadlift_df.lt(user_deadlift).sum()/len(deadlift_df)*100

print(squat_rank.to_string(index=False) + "%")
print(bench_rank.to_string(index=False) + "%")
print(deadlift_rank.to_string(index=False) + "%")

# html_content = driver.page_source
# driver.close()

# total_lifts = [sum(lifts) for lifts in zip(squats, benches, deadlifts)]
# total_lifts = list(np.around(np.array(total_lifts), 1))

# #calculating rank of lifter

# print(sorted(squats))
# print(sorted(benches))
# print(sorted(deadlifts))
# print(sorted(total_lifts))

# OUSTANDING TASKS:
# --> Backend
# --> Frontend
# - set up front end and inputs
# - logic for inputs and how they're categorized
# --> Features/Upgrades
# - Set up git hub
# - Account stuff
# - Unit tests using csv (update db again too)

#searching website that does not use API
# def get_html_content(equipment, weight_class, gender, age, category):
#     USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
#     LANGUAGE = "en-US,en;q=0.5"
#     session = requests.Session()
#     session.headers['User-Agent'] = USER_AGENT
#     session.headers['Accept-Language'] = LANGUAGE
#     session.headers['Content-Language'] = LANGUAGE
#     html_content = session.get(f'https://www.openpowerlifting.org/rankings/{equipment}/{weight_class}/{gender}/{age}/{category}')
#     return html_content

#html_content = get_html_content(equipment, weight_class, gender, age, category)

# #parser
# soup = BeautifulSoup(html_content, "html.parser")

# #sorting through parsed data
# squats = [user_squat]
# benches = [user_bench]
# deadlifts = [user_deadlift]

# top_squats = soup.find_all("span", attrs={"class": "squat"})
# top_benches = soup.find_all("span", attrs={"class": "bench"})
# top_deadlifts = soup.find_all("span", attrs={"class": "deadlift"})

# SORTING PARSED DATA bs4 ALTERNATIVE

# all_squat = soup.find_all(class_="slick-cell l11 r11")
# print(all_squat)

# all_squat = soup.find_all("span", class_="squat")
# print(all_squat)

# df = pd.DataFrame(list(zip(all_squat)), columns = lifts)
# print(df.head())

# BACKUP FULL
# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(options=options)
# driver.maximize_window()
# driver.get(f'https://www.openpowerlifting.org/rankings/\
# {equipment}/{weight_class}/{gender}/{age}/{category}')
# driver.implicitly_wait(15)

# # retrieving lift data
# # does not need to be run once all data stored in database

# i = 0
# squats = [user_squat]
# benches = [user_bench]
# deadlifts = [user_deadlift]

# squat_data = driver.find_elements(By.CLASS_NAME, "squat")
# bench_data = driver.find_elements(By.CLASS_NAME, "bench")
# deadlift_data = driver.find_elements(By.CLASS_NAME, "deadlift")

# for squat in squat_data:
#     squats.append(float(squat.text))
# for bench in bench_data:
#     benches.append(float(bench.text))
# for deadlift in deadlift_data:
#     deadlifts.append(float(deadlift.text))
# driver.execute_script("arguments[0].scrollIntoView(true);", squat_data[-1])
# time.sleep(0.1)

# while i <= 2:
#     squat_data = driver.find_elements(By.CLASS_NAME, "squat")
#     bench_data = driver.find_elements(By.CLASS_NAME, "bench")
#     deadlift_data = driver.find_elements(By.CLASS_NAME, "deadlift")
#     temp_squats = []
#     temp_benches = []
#     temp_deadlifts = []

#     for squat in squat_data:
#         temp_squats.append(float(squat.text))
#     for bench in bench_data:
#         temp_benches.append(float(bench.text))
#     for deadlift in deadlift_data:
#         temp_deadlifts.append(float(deadlift.text))

#     driver.execute_script("arguments[0].scrollIntoView(true);", squat_data[-1])
#     time.sleep(2)

#     temp_squats[0:7] = []
#     squats.extend(temp_squats)
#     temp_benches[0:7] = []
#     benches.extend(temp_benches)
#     temp_deadlifts[0:7] = []
#     deadlifts.extend(temp_deadlifts)

#     i = i + 1

# # #insert data into MongoDB
# # #only needs to be run once to store in DB, do not run otherwise

# client = MongoClient()
# client = MongoClient("localhost", 27017)

# db = client.PowerliftingDB

# # squats_dict = {}
# # squats_dict["squats"] = squats
# # # print(squats_dict)
# # benches_dict = {}
# # benches_dict["benches"] = benches
# # # print(benches_dict)
# # deadlifts_dict = {}
# # deadlifts_dict["deadlifts"] = deadlifts
# # # print(deadlifts_dict)

# # db.LiftData.insert_one(squats_dict)
# # db.LiftData.insert_one(benches_dict)
# # db.LiftData.insert_one(deadlifts_dict)

# #Calculate rank of user

# squat_df = pd.DataFrame(squats)
# bench_df = pd.DataFrame(benches)
# deadlift_df = pd.DataFrame(deadlifts)

# squat_rank = squat_df.lt(user_squat).sum()/len(squat_df)*100
# bench_rank = bench_df.lt(user_bench).sum()/len(bench_df)*100
# deadlift_rank = deadlift_df.lt(user_deadlift).sum()/len(deadlift_df)*100

# print(squat_rank.to_string(index=False) + "%")
# print(bench_rank.to_string(index=False) + "%")
# print(deadlift_rank.to_string(index=False) + "%")

# html_content = driver.page_source
# driver.close()
