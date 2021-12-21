"""
MAIN ALGORITHM FOR INFORMATION RETRIEVAL AND SCORE ASSEMBLY

The whole app rotates around the algorithm that,  once the user inserts his details,
will retrieve the required information about the country by means of online API‘s.
The script will also be able to translate the values obtained into a 10 points grade,
in order to be able to generate single scores representing more differ-ent topics.
"""

# ==========================================================================
# IMPORT AND ADAPT TO DJANGO REPOSITORY ACCESS LOGIC
# ==========================================================================
import requests

# django and python have 2 different way to look at directories, this command make the server and the test
# working simultaneously
try:
    from peaklife.settings import (
        indicators,
        indicators_female_youth,
        indicators_male_youth,
        indicators_female_adult,
        indicators_male_adult,
    )

except ModuleNotFoundError:
    from src.peaklife.settings import (
        indicators,
        indicators_female_youth,
        indicators_male_youth,
        indicators_female_adult,
        indicators_male_adult,
    )

# ==========================================================================
# FUNCTIONS
# ==========================================================================
def categorize(gender, age):
    """ The function gives information on what dictionary we should retrieve data from"""
    category_indicator = {}

    age_status = "youth"
    if int(age) > 25:
        age_status = "adult"
    if gender == "female" and age_status == "youth":
        category_indicator = indicators_female_youth
    if gender == "female" and age_status == "adult":
        category_indicator = indicators_female_adult
    if gender == "male" and age_status == "youth":
        category_indicator = indicators_male_youth
    if gender == "male" and age_status == "adult":
        category_indicator = indicators_male_adult

    return category_indicator


def get_indicators(label, gender, age):
    """ The function retrieves the information and prints a dictionary of results """

    result_dict = {}
    payload = "?$filter=SpatialDim eq '" + label + "'"
    url = "https://ghoapi.azureedge.net/api/"

    indicator_dict_lst = [indicators, categorize(gender, age)]

    # choose the correct indicator to retrieve the user detailed information
    for indicator_dict in indicator_dict_lst:
        grade_lst = []
        grade_weight_lst = []
        for indicator in indicator_dict:

            best_score = indicator_dict[indicator][1]
            worst_score = indicator_dict[indicator][2]
            indicator_key = indicator_dict[indicator][0]
            indicator_weight = indicator_dict[indicator][3]
            api_information = requests.get(url + indicator_key + payload)
            json_response = api_information.json()

            try:
                if indicator_dict == indicator_dict_lst[1]:
                    if gender == "male":
                        score = float((((json_response['value'][0])["Value"]).split(" "))[0])
                    else:  # if female
                        score = float((((json_response['value'][2])["Value"]).split(" "))[0])
                else:
                    score = float(
                        (((json_response["value"][0])["Value"]).split(" "))[0]
                    )
                grade = round(
                    (float(score) - worst_score) / (best_score - worst_score) * 10, 2
                )
                grade_lst.append(grade * indicator_weight)
                grade_weight_lst.append(indicator_weight)

            except (IndexError, ValueError):
                continue
        if grade_lst:
            score = round(sum(grade_lst) / sum(grade_weight_lst), 2)
        else:
            score = 0

        if indicator_dict == indicator_dict_lst[0]:
            result_dict["General Score"] = score
        if indicator_dict == indicator_dict_lst[1]:
            result_dict["User Tailored Score"] = score

    # getting final score
    if result_dict["User Tailored Score"] != 0:
        final_score = (
            result_dict["General Score"] * 0.4
            + result_dict["User Tailored Score"] * 0.6
        )
        result_dict["Total country score"] = round(final_score, 2)
    else:
        result_dict["Total country score"] = "No user detail inserted"
        result_dict["User Tailored Score"] = "No user detail inserted"

    return result_dict
