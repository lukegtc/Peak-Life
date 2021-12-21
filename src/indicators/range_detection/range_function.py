"""
Functions required for range retrieval
"""

import numpy as np
import requests
from tqdm import tqdm

#  ============================================================================================================
#  RANGE AND VALUE FUNCTION
#  ============================================================================================================
# this one finds the score of the country on the selected indicator
def value(country_code, url, gender):
    payload = "?$filter=SpatialDim eq '" + country_code + "'"
    r = requests.get(url + payload)
    json_response = r.json()
    if gender == 'female':
        value = (json_response['value'][2])["Value"]
    else:
        value = (json_response['value'][0])["Value"]
    return value

# now we will calculate the score for the male life expectancy and compare:
def range_count(country_list, indicator, gender):
    ind = 0
    scores = np.zeros(len(country_list))
    for i in tqdm(country_list, ascii=True, desc="Country value retrieval", ncols=100):
        try:
            url = "https://ghoapi.azureedge.net/api/" + indicator
            score_country = value(i[0], url, gender)
            try:
                scores[ind] = float((score_country.split(" "))[0])
                #print(f"{i[1]} scored {score_country}")
            except ValueError:
                #print(f"No data available for {i[1]}")
                scores[ind] = None
        except IndexError:
            #print(f"No data available for {i[1]}")
            scores[ind] = None
        ind += 1
    return np.nanmax(scores), np.nanmin(scores)
