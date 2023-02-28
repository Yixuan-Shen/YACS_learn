import requests
import json
from bs4 import BeautifulSoup


def parseHtmlToGetFacultyEmail(soup: BeautifulSoup) -> dict:
    # Get all emails
    Faculty = {}
    links = soup.find_all('a', href=True)
    for link in links:
        if link['href'].startswith('mailto:'):
            Faculty[link['href'][7:]] = link['target']
    return Faculty


def parseRCSID(Faculty: dict) -> list:
    RCSIDs = [email.split('@')[0] for email in Faculty]
    return RCSIDs


def loadCourseTreeWithRCSID(CourseTree: dict, AllFaculty: dict, session: requests.Session):
    for semester in CourseTree:
        for department in CourseTree[semester]:
            for course in CourseTree[semester][department]:
                for crn in CourseTree[semester][department][course]:
                    link = getCourseLink(semester, department, course, crn)
                    html = session.get(link)
                    soup = BeautifulSoup(html.text, 'html.parser')
                    facultys = parseHtmlToGetFacultyEmail(soup)
                    rcsIDs = parseRCSID(facultys)
                    CourseTree[semester][department][course][crn] = rcsIDs
                    for RCSID in rcsIDs:
                        AllFaculty[RCSID] = {}


def getCourseLink(semester: str, department: str, course: str, crn: str):
    link = 'https://sis.rpi.edu/rss/bwckschd.p_disp_listcrse?term_in={}&subj_in={}&crse_in={}&crn_in={}'.format(
        semester, department, course, crn)
    return link


def FillJSONWithRCSIDs(session) -> dict:
    Courses = dict()
    AllFaculty = dict()

    # Load course data from JSON file
    with open("Courses.json", 'r') as infile:
        Courses = json.load(infile)

    loadCourseTreeWithRCSID(Courses, AllFaculty, session)

    # Write to JSON file
    with open("Courses.json", 'w') as outfile:
        json.dump(Courses, outfile, indent=4, sort_keys=False)

    # with open("Prof.json", 'w') as outfile:
    #     json.dump(AllFaculty, outfile, indent=4, sort_keys=True)

    return AllFaculty


if __name__ == "__main__":
    session = requests.Session()
    FillJSONWithRCSIDs(session)
