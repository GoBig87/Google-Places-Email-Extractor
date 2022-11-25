# email-search
A python script for taking in a GPS rectangle and create sections inside
to break up a Google Maps api places search.  The search will take in search 
parameters to filter the search based on them.  If a business website is found
the script will attempt to parse a contact email address from the site.  If a
contact email address is found the results will be appended to a csv file.

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