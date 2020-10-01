from flask import Flask, render_template
import folium
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from flask_apscheduler import APScheduler
from clock import ma

app=Flask(__name__)
scheduler = APScheduler()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/covid_map")
def covid_map(ma):
    return ma





if __name__=="__main__":
    scheduler.add_job(id = 'Covid Map task',func= My_Map ,trigger = 'interval',  minutes=2)
    scheduler.start()
    app.run()  