"""Utility file to seed points database from tsv files in seed_data"""

from sqlalchemy import func
from models import Waypoint, Route
from models import connect_to_db, db
from server import app
import glob
import os
import re
import string
path = "./seed_data/*.tsv"


def load_waypoints():
    """ Load waypoints from all tsv in seed_data """

    print "Waypoints"

    # Delete all rows in table to prevent duplicates
    # in case of need to re-seed
    Waypoint.query.delete()

    # Read all .tsv files in seed_data and insert data
    for fname in glob.glob(path):
        with open(fname) as f:
            content = f.readlines()[1:]
            for row in content:
                row = row.rstrip()
                row = re.split(r'\t+', row)
                if "##" in row[-1]:
                    not_useful = row[-1].find("##")
                    if not_useful >= 32:
                        row[-1] = row[-1][:not_useful]
                if "NULL" in row[-1]:
                    continue
                if "Bound" in row[-1]:
                    continue

                lat_long = row[-1].split(",")
                lat = lat_long[0]
                lng = lat_long[-1]

                if '\xe2' in lat:
                    latitude = re.sub("`", "'", lat)
                elif '\xe2' in lng:
                    longitude = re.sub("`", "'", lng)

                latitude = lat
                longitude = lng

                latitude = dms2dec(lat)
                longitude = dms2dec(lng)
                longitude = -longitude

                point = [row[0], latitude, longitude]
                waypoint = Waypoint(latitude=point[1],
                                    longitude=point[2],
                                    location=point[0],
                                    )
                # Add waypoint to db session
                db.session.add(waypoint)
    # Commit waypoints
    db.session.commit()


def dms2dec(dms_str):
    """Return decimal representation of DMS
    >>> dms2dec(utf8(4853'10.18"N))
    48.8866111111F
    >>> dms2dec(utf8(220'35.09"E))
    2.34330555556F
    >>> dms2dec(utf8(4853'10.18"S))
    -48.8866111111F
    >>> dms2dec(utf8(220'35.09"W))
    -2.34330555556F
    """
    dms_str = re.sub(r'\s', '', dms_str)
    if re.match('[swSW]', dms_str):
        sign = -1
    else:
        sign = 1

    if "." not in dms_str:
        dms_str = dms_str[:-1] + ".00" + dms_str[-1] 
    (degree, minute, second, micro_seconds, trash) = re.split('\D+', dms_str, maxsplit=4)
    return sign * (int(degree) + float(minute)
                    / 60 + float(second) / 3600 + 
                    float(micro_seconds) / 36000)


##################################################################################


def load_routes():
    """ Seed Routes and Route_Waypoints with curated Routes """
    # Themes:
    themes = {1:"foodie", 2:"coffee", 3:"beer", 4:"weed",
              5:"history", 6:"architecture", 7:"art",
              8:"oddities", 9:"music", 10:"design", 11:"books"}

    # Easy (3-4 Waypoints):

    easy = {"route1":{"waypoints":[93,66,247,347],
            "route_difficulty":"easy", "route_type":themes[6],
            "description":"Historic houses of Hayes Valley."},
            "route2":{"waypoints":[201,315,45,244],
            "route_difficulty":"easy", "route_type":themes[5],
            "description":"Historic tour of North Beach."},
            "route3":{"waypoints":[95,182,21],
            "route_difficulty":"easy", "route_type":themes[5],
            "description":"Historic tour of Golden Gate Park and Ocean Beach."},
            # "route4":{"waypoints":[],
            # "route_difficulty":"easy", "route_type":,
            # "description":""},
            # "route5":{"waypoints":[],
            # "route_difficulty":"easy", "route_type":,
            # "description":""},
            # "route6":{"waypoints":[],
            # "route_difficulty":"easy", "route_type":,
            # "description":""},
            # "route7":{"waypoints":[],
            # "route_difficulty":"easy", "route_type":,
            # "description":""},
            # "route8":{"waypoints":[],
            # "route_difficulty":"easy", "route_type":,
            # "description":""},
            # "route9":{"waypoints":[],
            # "route_difficulty":"easy", "route_type":,
            # "description":""},
            # "route10":{"waypoints":[],
            # "route_difficulty":"easy", "route_type":,
            # "description":""},
            }


    # Medium (5-7 Waypoints):
    medium = {"route1":{"waypoints":[71,203,117,335,183,235,71],
              "route_difficulty":"medium", "route_type":themes[5],
              "description":"Historic tour of Nob Hill."},
              "route2":{"waypoints":[70,237,79,221,199,70],
              "route_difficulty":"medium", "route_type":themes[6],
              "description":"Historic Architecture of downtown San Francisco."},
              "route3":{"waypoints":[105,22,230,288,205],
              "route_difficulty":"medium", "route_type":themes[5],
              "description":"Historic tour of Golden Gate Park and Haight area."},
              # "route4":{"waypoints":[],
              # "route_difficulty":"medium", "route_type":,
              # "description":""},
              # "route5":{"waypoints":[],
              # "route_difficulty":"medium", "route_type":,
              # "description":""},
              # "route6":{"waypoints":[],
              # "route_difficulty":"medium", "route_type":,
              # "description":""},
              # "route7":{"waypoints":[],
              # "route_difficulty":"medium", "route_type":,
              # "description":""},
              # "route8":{"waypoints":[],
              # "route_difficulty":"medium", "route_type":,
              # "description":""},
              # "route9":{"waypoints":[],
              # "route_difficulty":"medium", "route_type":,
              # "description":""},
              # "route10":{"waypoints":[],
              # "route_difficulty":"medium", "route_type":,
              # "description":""},
            }


    # Hard (8-10+ Waypoints):
    # hard = {"route1":{"waypoints":[],
    #         "route_difficulty":"hard", "route_type":,
    #         "description":""},
    #         "route2":{"waypoints":[],
    #         "route_difficulty":"hard", "route_type":,
    #         "description":""},
    #         "route3":{"waypoints":[],
    #         "route_difficulty":"hard", "route_type":,
    #         "description":""},
    #         "route4":{"waypoints":[],
    #         "route_difficulty":"hard", "route_type":,
    #         "description":""},
    #         "route5":{"waypoints":[],
    #         "route_difficulty":"hard", "route_type":,
    #         "description":""},
    #         "route6":{"waypoints":[],
    #         "route_difficulty":"hard", "route_type":,
    #         "description":""},
    #         "route7":{"waypoints":[],
    #         "route_difficulty":"hard", "route_type":,
    #         "description":""},
    #         "route8":{"waypoints":[],
    #         "route_difficulty":"hard", "route_type":,
    #         "description":""},
    #         "route9":{"waypoints":[],
    #         "route_difficulty":"hard", "route_type":,
    #         "description":""},
    #         "route10":{"waypoints":[],
    #         "route_difficulty":"hard", "route_type":,
    #         "description":""},
    #         }


    # Iterate through and add routes:
    routes = [easy, medium] #add hard once 1 route exists

    for level in routes:
        for route in level:
            curr_route = level[route]
            print curr_route
            waypoints = curr_route["waypoints"]
            route_difficulty = curr_route["route_difficulty"]
            route_type = curr_route["route_type"]
            description = curr_route["description"]

            route = Route(waypoints=waypoints,
                          route_difficulty=route_difficulty,
                          route_type=route_type,
                          description=description)

            db.session.add(route)
    db.session.commit()


##################################################################################    

if __name__ == "__main__":
    connect_to_db(app)

    # # In case tables haven't been created, create them
    db.create_all()

    # Import data type
    load_waypoints()
    load_routes()

       