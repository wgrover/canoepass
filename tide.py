import requests
from datetime import datetime,timezone,timedelta
from zoneinfo import ZoneInfo
now = datetime.now(timezone.utc)
url = "https://api-iwls.dfo-mpo.gc.ca/api/v1/stations/5cebf1de3d0f4a073c4bb954/data?time-series-code="
url += "wlp"
url += "&from="
url += now.strftime("%Y-%m-%dT%H%%3A%M%%3A%SZ")
url += "&to="
future = now + timedelta(days=1)
url += future.strftime("%Y-%m-%dT%H%%3A%M%%3A%SZ")
response = requests.get(url)
times = []
heights = []
for row in response.json():
    utc = datetime.strptime(row["eventDate"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("UTC"))
    time = utc.astimezone(ZoneInfo("America/Vancouver"))
    times.append(time)
    heights.append(row["value"] * 3.28084)
print ("Current height is %0.1f feet." % heights[0])
if heights[0] >= 10.0:
    for time, height in zip(times, heights):
        if height < 10.0:
            print("OK to go until", time)
            break
else:
    for time, height in zip(times, heights):
        if height >= 10.0:
            print("No good until", time)
            break


