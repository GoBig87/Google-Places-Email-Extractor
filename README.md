# Google-Places-Email-Extractor
A python app for creating sectional search areas to break up a 
Google Maps api places search.  Inside the selected area, a search
radius can be applied to break the area up into multiple search
points.  Once the search area points have been calculated, input a file 
name to save the search data to.  Finally input your keyword and start the
search.  The results will be saved into a csv file containing the Google Places ID
and the extractred email.

# Install deps
```
python3 -m venv venv

source venv/bin/activate

pip install -r requirments.txt
```

# Running a search
Activate python virtual environment
```
source venv/bin/activate
```
then run the search with the app with
```
python main.py
```

# Adding Google API key
In order to make requests with the Google Places API users must input their Google API key
which can be found here https://developers.google.com/maps/documentation/places/web-service/get-api-key.
On the initial app launch, a screen will ask for your API key.  Paste it into the text field and click |
save.  Keys will be stored in ./.secrets/googlekey

![Screenshot from 2022-11-25 12-37-24](https://user-images.githubusercontent.com/39137894/204053386-62bffb82-04f6-497f-bd2c-60a19345ece2.png)
WARNING! Be sure to fully read the terms of service and understand the billing criteria. 
Any Google Places API data CANNOT be stored or cached other than the places ID.  Emails are obtained through scrapping
and are thus not subjected to the Googles terms of service.  Google Places API request also can invoke monetray costs
if used beyond the free tier.  Understand and monitor your account usage to avoid large bills. 
https://cloud.google.com/maps-platform/terms/

# Mapbox API key
In order to display the map, an API key is required from Mapbox which can be found here
https://docs.mapbox.com/api/accounts/tokens/ and be sure to read their terms of service
https://www.mapbox.com/legal/tos.  After adding your Google API key, another screen
will ask for your Mapbox API key. Paste it into the text field and click |
save.  Keys will be stored in ./.secrets/mapboxkey

![Screenshot from 2022-11-25 12-48-01](https://user-images.githubusercontent.com/39137894/204054037-935e7a19-9aab-483f-8fd9-bc45196ddfde.png)

# Performing a Search
On the map, right click to place a map marker where you would like to begin a search.

![Screenshot from 2022-11-25 12-53-41](https://user-images.githubusercontent.com/39137894/204054460-e6dc68ac-5280-453e-805a-25c8973da1c1.png)

Right click again to create a search area.

![Screenshot from 2022-11-25 12-53-54](https://user-images.githubusercontent.com/39137894/204054501-ba1672cb-340f-4dfd-a5f3-292743cc1dfc.png)

Click "Add Section" to add the current section to the search area.  Left click on the map marker to delete the marker and try again if the 
section needs to be adjusted. More sections can be added after clicking "Add Section" as shown below.

![Screenshot from 2022-11-25 12-58-10](https://user-images.githubusercontent.com/39137894/204054788-39e15c89-aeda-4654-9c61-c4ff78c08f83.png)

When all the sections have been added, enter the search radius (meters) that the area will be broken up into.  Then click "Calculate Search Points".
The app doesn't not search past one page of results, so if a more refined search is needed, reduce the search radius to limit results to one page.

![Screenshot from 2022-11-25 12-58-10](https://user-images.githubusercontent.com/39137894/204054982-5b0fa28e-05a9-4661-b2d3-5080ce3f9b7c.png)

Once the search points have been calculated enter the file name for results to be saved.  The search term can be left blank to search for everything or a term can be added to search with.

![Screenshot from 2022-11-25 13-04-06](https://user-images.githubusercontent.com/39137894/204055297-826da899-7679-44f8-8ec9-068f637a1143.png)

Then click "Start Search" which will launch a pop up that will display the search progress.

![Screenshot from 2022-11-25 13-12-30](https://user-images.githubusercontent.com/39137894/204055757-cff88ba5-0b01-4e08-be7c-7a8e78191a08.png)

Once the search has finished (or canceled) the result file will be saved into a csv file with the place id and email address.

# Settings

![Screenshot from 2022-11-25 13-19-41](https://user-images.githubusercontent.com/39137894/204056214-898e05c6-5ee6-431c-a621-e5923f298677.png)

# Gui Params
Toggle light or dark mode.  Some GUI widgets get stuck when toggle switching.  Restarting the app fixes the issue.

# API Keys
API keys can be updated/changed by clicking on the pencil

# App settings
You can clear the Google Places ID.  By default every search saves the Places ID into a cache file to skip over them on subsequent searches. 

# Disclaimer 
I wrote this App in two days.  There's probably bugs...  It works okayish for me but I'm sure issues will arise with more use.


