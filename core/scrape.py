from __future__ import print_function
#django rest framework connection to frontend
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse,JsonResponse,StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from .models import Powerlifting
from .serializer import PowerliftingSerializer

from cgitb import html
from numpy import double
from collections import defaultdict
# from bson import ObjectId
# import pip._vendor.requests
# import requests
# import re
import numpy as np

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

# Return user inputs
def main(request):
    return

# Hard coded user inputs
equipment = "raw"
weight = 160 
gender = "male"
if gender == "male":
    gender = "male"
    #need way to automatically categorize
    if weight > 145 and weight <= 163:
        weight_class = "ipf74"
    elif weight > 163 and weight <= 183:
        weight_class = "ipf83"
        pass
else:
    #automatic categorization needed here too
    gender = "female"
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

# grab_lift_data()

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

    if gender == "male":
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

# store_data()

# html_content = driver.page_source
driver.close()

