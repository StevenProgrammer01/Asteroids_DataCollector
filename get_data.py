import numpy as np
import pandas as pd
import requests as rq
import os 

url = r"https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=79eeSztX9APQsMaGTLKvOzil3rJHthbAhFcu3Qp2"
data = rq.get(url=url).text
file_n = 0
with open(f"data/file{file_n}.txt", "w") as file:
    file.write(data)
    file.close()

while file_n <= 1641:
    file_n += 1
    url = r"https://api.nasa.gov/neo/rest/v1/neo/browse?page={0}&size=20&api_key=79eeSztX9APQsMaGTLKvOzil3rJHthbAhFcu3Qp2".format(file_n)
    data = rq.get(url=url).text
    with open(f"data/file{file_n}.txt", "w") as file:
        file.write(data)
        file.close()
    print(data)
    

