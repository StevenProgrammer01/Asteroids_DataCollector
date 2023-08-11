import requests as rq
import pandas as pd
import numpy as np
dates = np.array(["01","08","15","22","29"])

date = 0
data = []
while date < len(dates)-1:
    url = r"https://api.nasa.gov/neo/rest/v1/feed?start_date=2022-07-{0}&end_date=2022-07-{1}&api_key=79eeSztX9APQsMaGTLKvOzil3rJHthbAhFcu3Qp2".format(dates[date],dates[date+1])
    res = rq.get(url=url).json()
    res
    data.append(res)
    date += 1

data_format = {

    "id":[],
    "name":[],
    "nasa_jpl_url":[],
    "estimated_diameter":[],
    "absolute_magnitude_h":[],
    "close_approach_data":[],
    "velocity":[],
    "miss_distance":[],
    "is_potentially_hazardous_asteroid":[],
    "is_sentry_object":[]
}
iterator = 0

while iterator < len(data):
    main_data = [i for i in data[iterator]["near_earth_objects"].values()]
    for i in main_data:
        for h in i:
            for j in h.keys():
                if j in data_format and j not in ["close_approach_data","estimated_diameter","links"]:
                    data_format[j].append(h[j])
                elif j == "estimated_diameter":
                    #if i[j]["meters"]["estimated_diameter_min"] == ""
                    data_format[j].append(h[j]["meters"]["estimated_diameter_min"])
                elif j == "close_approach_data":
                    data_format[j].append(h[j][0]["close_approach_date"])
                    data_format["velocity"].append(h[j][0]["relative_velocity"]["kilometers_per_second"])
                    data_format["miss_distance"].append(h[j][0]["miss_distance"]["kilometers"])
    iterator+=1
            


for i in data_format.values():
    print(len(i))
    #print("key:{0} value:{1}".format(i, data_format[i]))

dataframe = pd.DataFrame(data_format)

dataframe.to_csv("asteroids_data.csv", index=False)
