"""
VALUE RANGE DETECTOR FOR SPECIFIC INDICATOR

In order to bring all types of information retrieved from the indicators to a same
grading scale, a tool for the determination of ranges for each indicator is required.

Once the max and min values are retrieved, then a 10 point score can be assigned to
future value retrievals computed by the app.
"""

# ==========================================================================
# IMPORT AND ADAPT TO DJANGO REPOSITORY ACCESS LOGIC
# ==========================================================================
import sys

sys.path.insert(0, "../src")

try:
    from peaklife.settings import (
        indicators,
        indicators_female_youth,
        indicators_male_youth,
        indicators_female_adult,
        indicators_male_adult,
    )

    from indicators.range_detection import country_list
    from indicators.range_detection.range_function import range_count, value

except ModuleNotFoundError:
    from src.peaklife.settings import (
        indicators,
        indicators_female_youth,
        indicators_male_youth,
        indicators_female_adult,
        indicators_male_adult,
    )

    from src.indicators.range_detection import country_list
    from src.indicators.range_detection.range_function import range_count, value

#  ============================================================================================================
#  INPUT PROMPT FOR SINGLE INDICATOR
#  ============================================================================================================

# Input Prompt
country_list = country_list.country_list
indicator_input = input("insert your indicator --> ")
gender_input = input("insert the gender (if neutral then None) --> ")

#  ============================================================================================================
#  DICTIONARY RANGE UPDATE
#  ============================================================================================================
indicator_dicts = [indicators, indicators_female_youth, indicators_male_youth,
                   indicators_female_adult, indicators_male_adult]

indicator_found = False

for indicator_dict in indicator_dicts:
    for indicator in indicator_dict:
        code = indicator_dict.get(indicator)[0]
        if indicator_input == code and indicator_found is False:
            print("Indicator found! Updating range")
            print("... it might take some time ...\n")
            print(range_count(country_list, indicator_input, gender_input))
            indicator_found = True

if indicator_found is True:
    print("\nRange estimation completed! You can update the dictionary")

if indicator_found is False:
    print("\nThe indicator does not correspond to anything in the local database")
    print("Please update the dictionaries in src/peaklife/settings.py")
