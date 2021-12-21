"""
TESTING SCRIPT FOR PEAKLIFE ALGORITHM

The script is able to test the output dictionary of the get_indicators function.
It will also check the code coverage and the branch coverage of the script.

Check the README.md in this directory for step by step guide.
"""

# ==========================================================================
# IMPORT AND ADAPT TO DJANGO REPOSITORY ACCESS LOGIC
# ==========================================================================
from pylint import epylint as lint
import os

try:
    from indicators.algorithm import get_indicators
    from indicators.range_detection.range_function import range_count, value
    from indicators.range_detection import country_list
except ModuleNotFoundError:
    from src.indicators.algorithm import get_indicators
    from src.indicators.range_detection.range_function import range_count, value
    from src.indicators.range_detection import country_list

repository_path = os.path.dirname(os.path.abspath(__file__)).replace("/src/test", "")

# ==========================================================================
# TESTING FORMAT QUALITY OF ALGORITHM.PY AND GET_RANGE.PY
# ==========================================================================
print("\n======================== Format Quality ========================\n")
print(lint.py_run(repository_path + "/indicators/algorithm.py\n"))
print(lint.py_run(repository_path + "/indicators/range_detection/get_range.py"))


# ==========================================================================
# UNIT TEST OF ALGORITHM.PY
# ==========================================================================
def test_algorithm():
    """ test the outputs of the script"""
    assert len(get_indicators("ITA", "male", 34)) == 3  # check if correct inputs give a 3 line dictionary
    assert get_indicators("FRA", None, 18)['User Tailored Score'] == "No user detail inserted"  # check if the tailor made score
    assert get_indicators("FRA", None, 18)["Total country score"] == "No user detail inserted"
    assert get_indicators("ITA", 'female', 18)["Total country score"] != get_indicators("ITA", 'male', 18)["Total country score"]
    assert get_indicators("ITA", 'female', 18)["Total country score"] != get_indicators("ITA", 'female', 57)[
        "Total country score"]


# ==========================================================================
# CODE AND BRANCH COVERAGE EXECUTION
# ==========================================================================
print("\n======================== Testing for Coverage ========================\n")

def coverage():
    """ execute code for line and code coverage"""
    test_dict_algorithm = {
        "test_1": ("ITA", "male", 34),
        "test_2": ("AND", "female", 20),
        "test_3": ("FRA", None, 20),
        "test_4": ("BRA", "female", 46),
    }
    print("Checking coverage for algorithm.py")
    for test in test_dict_algorithm:
        label = test_dict_algorithm[test][0]
        gender = test_dict_algorithm[test][1]
        age = test_dict_algorithm[test][2]
        print(get_indicators(label, gender, age))

    test_dict_range = {
        "test_1": ('male'),
        "test_2": ('female')
    }

    print("\nChecking coverage for range_function.py")
    for test in test_dict_range:
        country = country_list.country_list
        test_indicator = "SA_0000001404"
        gender = test_dict_range[test][0]
        print(range_count(country, test_indicator, gender))

coverage()


