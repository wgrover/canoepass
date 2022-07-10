from flask import Flask, render_template
import requests
from datetime import datetime, timezone, timedelta
from backports.zoneinfo import ZoneInfo

app = Flask(__name__)

@app.route("/")
def index():
    now = datetime.now(timezone.utc) - timedelta(minutes=20)
    url = "https://api-iwls.dfo-mpo.gc.ca/api/v1/stations/5cebf1de3d0f4a073c4bb954/data?time-series-code=wlp&from="
    url += now.strftime("%Y-%m-%dT%H%%3A%M%%3A%SZ") 
    url += "&to="
    future = now + timedelta(days=1)
    url += future.strftime("%Y-%m-%dT%H%%3A%M%%3A%SZ")
    response = requests.get(url)
    times = []
    heights = []
    for row in response.json():
        utc = datetime.strptime(row["eventDate"], "%Y-%m-%dT%H:%M:%SZ")
        utc = utc + timedelta(minutes=20)
        utc = utc.replace(tzinfo=ZoneInfo("UTC"))
        time = utc.astimezone(ZoneInfo("America/Vancouver"))
        times.append(time)
        heights.append(row["value"] * 3.28084)
    print ("Current height is %0.1f feet." % heights[0])
    if heights[0] >= 10.0:
        for time, height in zip(times, heights):
            if height < 10.0:
                return render_template('index.html', floating=True, height=round(heights[0], 1), time=datetime.strftime(time, "%-I:%M %p on %A %B %-d %Y"))                
    else:
        for time, height in zip(times, heights):
            if height >= 10.0:
                return render_template('index.html', floating=False, height=round(heights[0], 1), time=datetime.strftime(time, "%-I:%M %p on %A %B %-d %Y")) 
