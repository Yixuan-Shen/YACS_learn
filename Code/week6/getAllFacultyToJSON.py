import requests
import json
from bs4 import BeautifulSoup

# link = https://sis.rpi.edu/rss/bwckschd.p_disp_listcrse?term_in=
# 202301&subj_in=CSCI&crse_in=2961&crn_in=80260


def parseRCSID(Faculty: dict) -> list:
    RCSIDs = [email.split('@')[0] for email in Faculty]
    return RCSIDs


def getFacultyInfo(RCSID: str, OriginalName: list = [False]) -> dict:
    html = requests.get('https://directory.rpi.edu/pplsearch/NULL/NULL/{}/NULL'
                        .format(RCSID))
    soup = BeautifulSoup(html.text, 'html.parser')
    rawInfo = soup.find_all('div', class_='row p-3 odd')
    if len(rawInfo) == 0:
        # print("Nothing found for this RCSID: " + RCSID)
        return {}
    rawInfo = rawInfo[0]
    Info = {}

    rawInfo = rawInfo.text
    rawInfo = rawInfo.split('\n')
    for i in range(len(rawInfo)):
        rawInfo[i] = rawInfo[i].strip()
    while '' in rawInfo:
        rawInfo.remove('')

    if OriginalName[0]:
        facultyName = OriginalName[1]
        pass
    else:
        facultyName = rawInfo[0]
    Email = ''
    Phone = ''
    Department = ''
    Portfolio = ''
    Title = rawInfo[1]
    for i in range(len(rawInfo)):
        if rawInfo[i].startswith('Email'):
            Email = rawInfo[i][7:]
        elif rawInfo[i].startswith('Phone'):
            Phone = rawInfo[i][7:]
        elif rawInfo[i].startswith('Department'):
            Department = rawInfo[i+1]
        elif rawInfo[i].startswith('Portfolio'):
            Portfolio = rawInfo[i+1]
    Info['Name'] = facultyName
    Info['Title'] = Title
    Info['Email'] = Email
    Info['Phone'] = Phone
    Info['Department'] = Department
    Info['Portfolio'] = Portfolio
    Info['Profile Page'] = verifyProfilePageLink(facultyName)
    # Info['Classes'] = []
    return Info


# TODO: Verify Profile Page link
def verifyProfilePageLink(facultyName: str) -> str:
    link = "https://faculty.rpi.edu/" + \
        facultyName.replace(' ', '-')
    html = requests.get(link)
    if html.status_code == 200:
        return link
    elif html.status_code == 404:
        return ""


def getCourseLink(semester: str, department: str, course: str, crn: str):
    link = '''https://sis.rpi.edu/rss/bwckschd.p_disp_listcrse?term_in={}&subj_in={}&crse_in={}&crn_in={}'''.format(
        semester, department, course, crn)
    return link


def getFacultyName(link: str) -> str:
    html = requests.get(link)
    soup = BeautifulSoup(html.text, 'html.parser')
    facultyName = 'a'
    return facultyName


def FacultyToJSON():
    AllFaculty = dict()

    # Load course data from JSON file
    with open("Courses.json", 'r') as infile:
        CourseTree = json.load(infile)

    for semester in CourseTree:
        for department in CourseTree[semester]:
            for course in CourseTree[semester][department]:
                for crn in CourseTree[semester][department][course]:
                    for RCSID in CourseTree[semester][department][course][crn]:
                        if RCSID not in AllFaculty:
                            AllFaculty[RCSID] = getFacultyInfo(RCSID)
                            if AllFaculty[RCSID] == {}:
                                print("Nothing found for this RCSID: " + RCSID)
                                AllFaculty.pop(RCSID)
                            #     print(semester, department, course, crn, RCSID)

    # # Write to JSON file
    with open('Prof.json', 'w') as outfile:
        json.dump(AllFaculty, outfile, indent=4, sort_keys=False)


if __name__ == "__main__":
    FacultyToJSON()
    # AllFaculty = dict()

    # # Load course data from JSON file
    # with open("Courses.json", 'r') as infile:
    #     # with open("2023 spring\RCOS\YACS_learn\Code\week6\Courses.json", 'r') as infile:
    #     CourseTree = json.load(infile)

    # for semester in CourseTree:
    #     for department in CourseTree[semester]:
    #         for course in CourseTree[semester][department]:
    #             for crn in CourseTree[semester][department][course]:
    #                 for RCSID in CourseTree[semester][department][course][crn]:
    #                     if RCSID not in AllFaculty:
    #                         AllFaculty[RCSID] = getFacultyInfo(RCSID)
    #                         # if AllFaculty[RCSID] == {}:
    #                         #     print(semester, department, course, crn, RCSID)

    # # # Write to JSON file
    # with open('Prof.json', 'w') as outfile:
    #     json.dump(AllFaculty, outfile, indent=4, sort_keys=False)

    # # print("Done")
