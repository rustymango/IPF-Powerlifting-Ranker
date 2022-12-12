from __future__ import print_function
# django rest framework connection to frontend
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "powerlifting_app.settings")

import django
django.setup()

from django.core.management import call_command
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse,JsonResponse,StreamingHttpResponse
from django.contrib.auth.models import User, Permission
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from .permissions import HasGroupPermission

from .models import Powerlifting
from .serializer import PowerliftingSerializer

from cgitb import html
from numpy import double
from collections import defaultdict
from bson import ObjectId
import pip._vendor.requests
import requests
import re
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

# Front-end inputs

# class RankView(viewsets.ModelViewSet):
#     serializer_class = RankSerializer

# # Query db

def query_lift_db(weight_class, database_id):
    
    client = MongoClient()
    client = MongoClient("localhost", 27017)

    db = client.PowerliftingDB    
    
    # global squats, benches, deadlifts

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
    
    return squats, benches, deadlifts

# Calculate rank of user

def calculate_rank(weight, gender, age, user_squat, user_bench, user_deadlift):
    if gender == "male":
        #need way to automatically categorize
        if int(weight) > 145 and int(weight) <= 163:
            weight_class = "ipf74"
        elif int(weight) > 163 and int(weight) <= 183:
            weight_class = "ipf83"
        else:
            weight_class = "ipf83" 
    else:
        if int(weight) > 138 and weight <= 152:
            weight_class = "ipf69"
        elif int(weight) > 152 and weight <= 168:
            weight_class = "ipf76"
        else:
            weight_class = "ipf76"

    if gender == "male":
        if age > 20 and age <= 23:
        # if age == "20-23":
            database_id = "MenJunior"
        else:
            database_id = "MenSenior"
    else:
        if age > 20 and age <= 23:
            database_id = "WomenJunior"
        else:
            database_id = "WomenSenior"
    
    # print(weight_class, database_id)

    squats, benches, deadlifts = query_lift_db(weight_class, database_id)

    squat_df = pd.DataFrame(squats)
    bench_df = pd.DataFrame(benches)
    deadlift_df = pd.DataFrame(deadlifts)

    squat_rank = squat_df.lt(user_squat).sum()/len(squat_df)*100
    bench_rank = bench_df.lt(user_bench).sum()/len(bench_df)*100
    deadlift_rank = deadlift_df.lt(user_deadlift).sum()/len(deadlift_df)*100

    print(squat_rank.to_string(index=False) + "%")
    print(bench_rank.to_string(index=False) + "%")
    print(deadlift_rank.to_string(index=False) + "%")

    squat_rank = squat_rank.to_string(index=False)
    bench_rank = bench_rank.to_string(index=False)
    deadlift_rank = deadlift_rank.to_string(index=False)

    return squat_rank, bench_rank, deadlift_rank

print(calculate_rank(160, "male", 22, 335, 285, 435))


@api_view(['GET', 'POST'])
def PowerliftingView(request, format=None):

    if request.method == 'GET':
        rank = Powerlifting.objects.all()
        serializer = PowerliftingSerializer(rank, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # serializer = PowerliftingSerializer(data = request.POST) 
        # print(request.POST)

        weight = request.data.get('weight', 162)
        gender = request.data.get('gender', "male")
        age = request.data.get('age', 22)
        user_squat = request.data.get('user_squat', 335)
        user_bench = request.data.get('user_bench', 285)
        user_deadlift = request.data.get('user_deadlift', 435)

        squat_rank, bench_rank, deadlift_rank = calculate_rank(int(weight), gender, int(age), int(user_squat), int(user_bench), int(user_deadlift))
        squat_rank = str(squat_rank) + "%"
        bench_rank = str(bench_rank) + "%"
        deadlift_rank = str(deadlift_rank) + "%"

        serializer = PowerliftingSerializer(data = {"weight": weight, "gender": gender, "age": age, "squat": user_squat, "bench": user_bench, "deadlift": user_deadlift, "squat_rank": squat_rank, "bench_rank": bench_rank, "deadlift_rank": deadlift_rank})

        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # print(squat_rank)
        # return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def rankDetail(request, pk, format=None):

    try:
        rank = Powerlifting.objects.get(pk=pk)
    except Powerlifting.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PowerliftingSerializer(rank)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PowerliftingSerializer(rank, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        rank.delete()
        return HttpResponse(status=204)