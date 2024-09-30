import requests
import json
import regex as re
import sys

BASE_URL = "https://api.kth.se/api/kopps/v2/course"

# Fetch course information from KTH API
def fetch_course(course_code):
    url = f"{BASE_URL}/{course_code}/detailedinformation"
    response = requests.get(url)
    with open(f"{course_code}.json", "w") as f:
        f.write(json.dumps(response.json(), indent=4))
    return response.json()

# Read course information from json file
def get_course(course_code):
    with open(f"{course_code}.json", "r") as f:
        return json.load(f)

# Get course name from course information
def get_course_name(course_code):
    course_raw = get_course(course_code)
    return course_raw['course']['title']  

# Get prerequisites from course information
def get_prerequisites(course_code):
    course_raw = get_course(course_code)
    try:
        return parse_prerequisites(course_raw['publicSyllabusVersions'][0]['courseSyllabus']['eligibility']) 
    except KeyError:
        print("No prerequisites found")
        return None

def parse_prerequisites(prerequisites):
    # Regular expression to extract course codes
    #Example course code: "DD1351" or "SF162D"
    course_code_pattern = r"[A-Z]{2}\d{3}\d?[A-Z]?(?:/[A-Z]{2}\d{3}\d?[A-Z]?)*"
    matches = re.findall(course_code_pattern, prerequisites)
    # Need to beautify the output. Make list of lists:
    lists = [match.split('/') for match in matches]
    return lists



def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py {course_code}")
        sys.exit(1)

    # Take argument and assign as course code
    course_code = sys.argv[1]

    # Fetch course information and save to json file
    fetch_course(course_code)

    # Read course information from json file
    course_name = get_course_name(course_code)
    prerequisites = get_prerequisites(course_code)
    print(f"Course name for {course_code} is {course_name}")
    print(f"Prerquisites for {course_code} are {prerequisites}")

if __name__ == "__main__":
    main()