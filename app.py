from flask import Flask, render_template
import folium
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

def clean_word(L):
    a=[]
    for word in L:
        if len(word)>2:
            a.append(word)
    return " ".join(a)

def My_Map():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_driver_path = 'C:\drivers\chromedriver.exe'
    #'''executable_path = os.environ.get("CHROMEDRIVER_PATH")'''
    browser = webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chrome_options)
    browser.get("https://m.le360.ma/covidmaroc/")
    html = browser.page_source
    browser.quit()
    soup = BeautifulSoup(html,'html.parser')
    list_table=soup.find_all('table', class_='table table-bordered dataTable')[0].find('tbody').find_all('tr')

    mytable=[]
    for row in list_table:
        row=row.find_all('td')
        name = clean_word(row[0].find('span').text.split(' ')).split('\u200b')[0]
        if(row[1].text==''):
        	cas=0
        else:
        	cas = int(row[1].text)
        if(row[2].text[1:]==''):
            cast_24=0
        else:
        	cast_24 = int(row[2].text[1:])
        if(row[3].text[1:]==''):
        	dead_24=0
        else:
        	dead_24 = int(row[3].text[1:])
        mytable.append({'name': name , 'cas': cas , 'cas_24': cast_24, 'dead_24':dead_24 })
    regions_loc = [
        {'name': 'Oriental',
        'latitude': 34.21063161705621,
        'longitude': -2.2398292872475123},
        {'name': 'Tanger Tetouan Al Hoceima',
        'latitude': 35.21648916999964,
        'longitude': -5.46061811161441},
        {'name': 'Guelmim Oued Noun',
        'latitude': 28.537079417694862,
        'longitude': -10.21129615427537},
        {'name': 'Dakhla-Oued Ed Daha',
        'latitude': 23.187768662138904,
        'longitude': -14.576887039381933},
        {'name': 'Beni Mellal-Khénifra',
        'latitude': 32.35536866706775,
        'longitude': -6.354611221480209},
        {'name': 'Darâa-Tafilalet',
        'latitude': 30.849663419282095,
        'longitude': -5.281174310301617},
        {'name': 'Marrakech Safi',
        'latitude': 31.658566001930208,
        'longitude': -8.50060605705501},
        {'name': 'Grand Casablanca-Settat',
        'latitude': 33.09434328504623,
        'longitude': -7.5835225431320215},
        {'name': 'Fès meknes',
        'latitude': 33.81997585277711,
        'longitude': -4.635183604212562},
        {'name': 'Laâyoune-Sakia El Hamra',
        'latitude': 26.150695319294833,
        'longitude': -12.827810335977418},
        {'name': 'Rabat Salé Kenitra',
        'latitude': 34.03819378608868,
        'longitude': -6.373051694854541},
        {'name': 'Souss-Massa',
        'latitude': 29.911104363087805,
        'longitude': -8.683976891847944}
    ]
    L=[]
    for i in range(12):
        for j in range(12):
            if(regions_loc[i]['name'][0:5]==mytable[j]['name'][0:5]):
                mytable[j]['name'] = regions_loc[i]['name']
                mytable[j]['latitude'] = regions_loc[i]['latitude']
                mytable[j]['longitude'] = regions_loc[i]['longitude']
                L.append(mytable[j])
                continue
    df = pd.DataFrame(L)
    global ma
    ma = folium.Map(location=[30, -10], zoom_start=5, min_zoom=4, max_zoom=7,tiles="cartodbpositron")
    geo = "https://raw.githubusercontent.com/Salah-Zkara/Morocco-GeoJson/master/Morocco-Regions.json"
    folium.Choropleth(
        geo_data=geo,
        name='COVID-19',
        data=df,
        columns=['name', 'cas'],
        key_on='feature.properties.nom_region',
        fill_color='OrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Total de cas confirmé',
    ).add_to(ma)
    def plotDot(point):
        html ="<center>"+str(point['name'])+"</center>"+"<br>"+"<font color='#d95e00'>"+"<b>"+str(point['cas'])+"</b>"+"</font>"+" Total de cas confirmé.<br>"+"<font color='#e6b01c'>"+"<b>"+str(point['cas_24'])+"</b>"+"</font>"+" Cas contaminés aujourd'hui.<br>"+"<font color='#cc0c0c'>"+"<b>"+str(point['dead_24'])+"</b>"+"</font>"+" Décès aujourd'hui.<br>"
        iframe = folium.IFrame(html,
                        width=250,
                        height=120)
        folium.CircleMarker(location=[point.latitude, point.longitude],
                            radius=24,
                            weight=0,
                            popup = folium.Popup(iframe),
                            fill_color='#000000',
                            fill_opacity=0,
                            line_opacity=0
                        ).add_to(ma)
    df.apply(plotDot, axis = 1)
    ma.fit_bounds(ma.get_bounds())
    #ma.save('templates/map.html')
    #print("DONE")

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/covid_map")
def covid_map():
    My_Map()
    return ma.get_root().render()

@app.route("/loading")
def loading():
    return render_template("loading.html")

if __name__=="__main__":
    app.run()  
