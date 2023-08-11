import numpy as np
import pandas as pd
import requests as rq

"""
This class is for the usage of the NeowS Open API from NASA
"""
class Asteroids():
    def __init__(self)->None:
        self.months = np.array(["01","02","03","04","05","06","07","08","09","10","11","12"])
        #This lambda function is for filter the day numbers and bring it's specific format
        self.days = np.array(list(map(lambda x: f"0{x}" if (x < 10)else str(x), range(1,32))))
        
    
    def aPerYear(self,year):
        """
        This function try to catch all the NeoWs Asteroids from a range of days. (01-29) of all
        """
        year = year
        days = np.array(list(map(lambda x: f"0{x}" if (x < 10)else str(x), range(1,32,7))))
        f_days = np.array(list(map(lambda x: f"0{x}" if (x < 10)else str(x), range(1,28,5))))
        
        data = []
        for i in self.months:
            date = 0
            while date < len(days)-1:
                if i == "02":
                    url = r"https://api.nasa.gov/neo/rest/v1/feed?start_date={0}-{1}-{2}&end_date={0}-{1}-{3}&api_key=79eeSztX9APQsMaGTLKvOzil3rJHthbAhFcu3Qp2".format(str(year),i,f_days[date],f_days[date+1])
                else:
                    url = r"https://api.nasa.gov/neo/rest/v1/feed?start_date={0}-{1}-{2}&end_date={0}-{1}-{3}&api_key=79eeSztX9APQsMaGTLKvOzil3rJHthbAhFcu3Qp2".format(str(year),i,days[date],days[date+1])
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
        iterator = 1

        while iterator <= len(data):
            main_data = [i for i in data[iterator-1]["near_earth_objects"].values()]
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

        try:
            dataframe = pd.DataFrame(data_format)
            dataframe.to_csv(f"asteroids_data_{year}.csv", index=False)
        except:
             print(f"Currently unavailable for {year}")
        
asteroids = Asteroids()

print(asteroids.days)
asteroids.aPerYear(2020)