import requests
import json
from bs4 import BeautifulSoup


def parseHtmlToGetFacultyEmail(soup: BeautifulSoup) -> dict:
    # html = open(filename, 'r')
    # soup = BeautifulSoup(html, 'html.parser')

    # Get all emails
    Faculty = {}
    links = soup.find_all('a', href=True)
    for link in links:
        if link['href'].startswith('mailto:'):
            # print(link['href'][7:], link['target'])
            Faculty[link['href'][7:]] = link['target']
    return Faculty


def parseRCSID(Faculty: dict) -> list:
    RCSIDs = [email.split('@')[0] for email in Faculty]
    return RCSIDs


def loadCourseTreeWithRCSID(CourseTree: dict):
    for semester in CourseTree:
        for department in CourseTree[semester]:
            for course in CourseTree[semester][department]:
                for crn in CourseTree[semester][department][course]:
                    link = getCourseLink(semester, department, course, crn)
                    html = requests.get(link)
                    soup = BeautifulSoup(html.text, 'html.parser')
                    facultys = parseHtmlToGetFacultyEmail(soup)
                    rcsID = parseRCSID(facultys)
                    CourseTree[semester][department][course][crn] = rcsID
        #             print(semester, department, course, crn, rcsID)
        #             break
        #         break
        #     break
        # break


def getCourseLink(semester: str, department: str, course: str, crn: str):
    link = 'https://sis.rpi.edu/rss/bwckschd.p_disp_listcrse?term_in={}&subj_in={}&crse_in={}&crn_in={}'.format(
        semester, department, course, crn)
    return link


def FillJSONWithRCSIDs():
    Courses = dict()

    # Load course data from JSON file
    with open("Courses.json", 'r') as infile:
        Courses = json.load(infile)

    loadCourseTreeWithRCSID(Courses)

    # Write to JSON file
    with open("Courses.json", 'w') as outfile:
        json.dump(Courses, outfile, indent=4, sort_keys=False)


if __name__ == "__main__":
    FillJSONWithRCSIDs()
    # Courses = dict()

    # # Load course data from JSON file
    # with open("Courses.json", 'r') as infile:
    #     # with open("2023 spring\RCOS\YACS_learn\Code\week6\Courses.json", 'r') as infile:
    #     Courses = json.load(infile)

    # loadCourseTreeWithRCSID(Courses)

    # # Write to JSON file
    # with open("Courses.json", 'w') as outfile:
    #     # with open("2023 spring\RCOS\YACS_learn\Code\week6\Courses.json", 'w') as outfile:
    #     json.dump(Courses, outfile, indent=4, sort_keys=False)

    # print("Done")
