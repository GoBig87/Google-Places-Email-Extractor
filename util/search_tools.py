import csv
import json
import math
import os
import re
import time
import traceback

import googlemaps
import requests

contact_regex = r'(href=[\'"]?contact([^\'" >]+)")'
email_regex = r'(([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+))'
ignore_ext = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi",
              ".png", ".gif", ".webp", ".tiff", ".tif", ".bmp",
              ".dib", ".svg", ".svgz", "/"]


def create_search_points(start_lat, end_lat, start_lon, end_lon, search_radius):
    """
    :param start_lat: gps float
    :param end_lat: gps float
    :param start_lon: gps float
    :param end_lon: gps float
    :param search_radius: float meters
    :return:
    list of gps points (tuple) to search with the Google api places
    """
    step_size = 2*search_radius/1.414
    distance_length = calculate_gps_distance(start_lat, end_lat, start_lon, start_lon)
    distance_height = calculate_gps_distance(start_lat, start_lat, start_lon, end_lon)
    num_lat_steps = math.ceil(distance_length/step_size)
    num_lon_steps = math.ceil(distance_height/step_size)
    gps_lat_step = (start_lat-end_lat)/num_lat_steps
    gps_lon_step = (start_lon-end_lon)/num_lon_steps

    if start_lat > end_lat:
        if end_lat < 0:
            lat_dir = 1
        else:
            lat_dir = -1
    else:
        if end_lat < 0:
            lat_dir = -1
        else:
            lat_dir = 1

    if start_lon > end_lon:
        if end_lon < 0:
            lon_dir = 1
        else:
            lon_dir = -1
    else:
        if end_lon < 0:
            lon_dir = -1
        else:
            lon_dir = 1

    ret_pts = []
    first_lat_pt = 0.5*gps_lat_step*lat_dir + start_lat
    first_lon_pt = 0.5*gps_lon_step*lon_dir + start_lon
    ret_pts.append([first_lat_pt, first_lon_pt])
    for i in range(0, num_lat_steps):
        current_lat = lat_dir*gps_lat_step*i + first_lat_pt
        for j in range(0, num_lon_steps):
            current_lon = lon_dir*gps_lon_step*j + first_lon_pt
            ret_pts.append([current_lat, current_lon])

    # Debugging, plot the output on this website https://mobisoftinfotech.com/tools/plot-multiple-points-on-map/
    # for pt in ret_pts:
    #     print(str(pt).replace(" ", "").strip("[").strip("]")+',#00FF00,marker,""')
    return ret_pts


def calculate_gps_distance(lat1, lat2, lon1, lon2):
    R = 6371  # radius of the earth in km
    x = (math.radians(lon2) - math.radians(lon1)) * math.cos(0.5 * (math.radians(lat2) + math.radians(lat1)))
    y = math.radians(lat2) - math.radians(lat1)
    distance = R * math.sqrt(x * x + y * y)
    return distance*1000


def search_places(points, radius, keyword="", key="", gui_update=None, request_cancel=None, return_callback=None):
    gmaps_client = googlemaps.Client(key=key)

    business_emails = []
    place_ids = load_place_ids()
    try:
        total = len(points)
        count = 0
        for point in points:
            count = count + 1
            if keyword:
                place = googlemaps.client.places_nearby(gmaps_client, location=point, radius=radius, keyword=keyword)
            else:
                place = googlemaps.client.places_nearby(gmaps_client, location=point, radius=radius)
            for result in place.get("results", []):
                if request_cancel:
                    if request_cancel(business_emails):
                        return business_emails
                if result.get("place_id", None):
                    name = result.get("name", "")
                    id = result["place_id"]
                    if id in place_ids:
                        continue
                    if gui_update:
                        gui_update(name, "Searching", "", "", count, total)
                    place_ids.append(id)
                    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={id}&key={key}&fields=website,formatted_address"
                    rsp = requests.get(url)
                    if rsp.status_code == 200:
                        data = rsp.json()
                        website = data.get("result", {}).get("website", "")
                        if not website:
                            print(f"no website for {name}.  skipping")
                            if gui_update:
                                gui_update(name, "Not Found", "Not Found", "Skipping", count, total)
                            continue
                        formatted_address = data.get("result", {}).get("formatted_address", "")
                        if gui_update:
                            gui_update(name, formatted_address, website, "Searching", count, total)
                        email_addr = find_regex_html(website, email_regex, ignore_ext)
                        if not email_addr:
                            contact_href = find_regex_html(website, contact_regex)
                            if contact_href:
                                href = contact_href.replace("href=", "").replace('"', '')
                                if "http" in href:
                                    href_url = href
                                else:
                                    href_url = f"{website}/{href}"
                                email_addr = find_regex_html(href_url, email_regex, ignore_ext)
                            else:
                                # make one last try for website/contact
                                href_url = f"{website}/contact"
                                email_addr = find_regex_html(href_url, email_regex, ignore_ext)
                        if email_addr:
                            row = build_csv_row(name, id, email_addr, formatted_address)
                            business_emails.append(row)
                            if gui_update:
                                gui_update(name, formatted_address, website, email_addr, count, total)
                        else:
                            if gui_update:
                                gui_update(name, formatted_address, website, "Not Found", count, total)
                            print(f"unable to find email address for {name} {website}")

    except Exception as error:
        print(traceback.print_exc())

    append_places_id(place_ids)
    if return_callback:
        return_callback(business_emails)
    return business_emails


def load_place_ids():
    place_ids = []
    if os.path.isfile("cache.json"):
        with open("cache.json") as f:
            place_ids = json.loads(f.read())
    return place_ids


def append_places_id(place_ids):
    if os.path.isfile("cache.json"):
        with open("cache.json") as f:
            stored_ids = json.loads(f.read())
        place_ids.append(stored_ids)
    with open("cache.json", "w") as f:
        f.write(json.dumps(place_ids))


def build_csv_row(name, place_id, email, formatted_address):
    split_address = formatted_address.split(", ")
    if len(split_address) == 5:
        addr = split_address[1]
        city = split_address[2]
        state_zip = split_address[3]
        try:
            state, zipcode = state_zip.split(" ")
        except:
            state = zipcode = ""
    elif len(split_address) == 4:
        addr = split_address[0]
        city = split_address[1]
        state_zip = split_address[2]
        try:
            state, zipcode = state_zip.split(" ")
        except:
            state = zipcode = ""
    else:
        addr = city = state = zipcode = ""

    print(f"found email for:  {name},{place_id},{email},{addr},{city},{state},{zipcode}")
    #  return [name, place_id, email, addr, city, state, zipcode]
    return [place_id, email]


def find_regex_html(url, regex, false_hit_chars=[]):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        rsp = requests.get(url, headers=headers, timeout=10)
    except:
        print(f"unable to find email address for {url}")
        return None
    if rsp.status_code == 200:
        matches = re.findall(regex, rsp.text)
        if not matches:
            return None
        for match in matches:
            if false_hit_chars:
                char_found = False
                for char in false_hit_chars:
                    if char in match[0]:
                        char_found = True
                if char_found:
                    break
                return match[0]
            else:
                return match[0]
    return None


def make_csv_file(file, rows):
    if not file.endswith(".csv"):
        file = file + ".csv"
    with open(file, 'w') as f:
        writer = csv.writer(f)
        #writer.writerow(["name", "place_id", "email", "address", "city", "state", "zipcode"])
        writer.writerow(["place_id", "email"])
        for row in rows:
            writer.writerow(row)


def start_search(args):
    # Create a list of search points
    search_points = create_search_points(
        args["start_lat"],
        args["end_lat"],
        args["start_lon"],
        args["end_lon"],
        args["search_radius"],
    )
    # Send list of search points to query Google Maps places
    parsed_info = search_places(
        search_points,
        args["search_radius"],
        args["keyword"],
    )
    make_csv_file(args["file_name"], parsed_info)


if __name__ == "__main__":
    start_lat = 28.060950 #float(sys.argv[1])
    end_lat = 27.961229 #float(sys.argv[2])
    start_lon = -82.836441  #float(sys.argv[3])
    end_lon = -82.783890 #float(sys.argv[4])
    #  search radius in meters
    search_radius = 1000 #float(sys.argv[5])
    file_name = f"business_search_tampa_bay_{int(time.time())}.csv"

    args = {
        "start_lat": start_lat,
        "end_lat": end_lat,
        "start_lon": start_lon,
        "end_lon": end_lon,
        "search_radius": search_radius,
        "file_name": file_name,
        "keyword": "",
    }
    start_search(args)
