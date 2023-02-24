import requests
import json
from bs4 import BeautifulSoup

# link = https://sis.rpi.edu/rss/bwckschd.p_disp_listcrse?term_in=
# 202301&subj_in=CSCI&crse_in=2961&crn_in=80260

# RCOS.html = https://sis.rpi.edu/rss/bwckschd.p_disp_listcrse?
# term_in=202301&subj_in=CSCI&crse_in=2961&crn_in=80260

# term_in=202301&
# subj_in=CSCI&
# crse_in=2961&
# crn_in=80260


def parseHtml(filename='RCOS.html') -> dict:
    html = open(filename, 'r')
    soup = BeautifulSoup(html, 'html.parser')

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


def getFacultyInfo(RCSID: str, facultyName: str) -> dict:
    html = requests.get('https://directory.rpi.edu/pplsearch/NULL/NULL/{}/NULL'
                        .format(RCSID))
    soup = BeautifulSoup(html.text, 'html.parser')
    rawInfo = soup.find_all('div', class_='row p-3 odd')[0]
    Info = {}
    Info['Name'] = facultyName
    Info['Title'] = rawInfo.contents[3].contents[0].strip()
    Info['Email'] = rawInfo.contents[5].contents[1].contents[1].next
    Info['Phone'] = rawInfo.contents[5].contents[5].next[7:]
    Info['Department'] = rawInfo.contents[7].contents[1].contents[1].next.strip()
    Info['Portfolio'] = rawInfo.contents[7].contents[3].contents[1].next.strip()
    Info['Classes'] = []
    return Info


def getCourseInfo():
    pass


# term_in=202301&
# subj_in=CSCI&
# crse_in=2961&
# crn_in=80260
def createCourseTree():
    courseTree = dict()
    courseTree['202301'] = dict()
    semesterCourseTree = courseTree['202301']
    semesterCourseTree['CSCI'] = dict()
    semesterCourseTree['CSCI']['2961'] = dict()
    semesterCourseTree['CSCI']['2961']['80260'] = (rcsID)
    return courseTree


if __name__ == "__main__":
    # Info = {}
    # Faculty = parseHtml()
    # RCSIDs = parseRCSID(Faculty)
    # i = 0
    # for people in Faculty:
    #     Info[RCSIDs[i]] = getFacultyInfo(RCSIDs[i], Faculty[people])
    #     i += 1

    # print(Info)
    # print('Done')

    # # Write to JSON file
    # with open('Prof.json', 'w') as outfile:
    #     json.dump(Info, outfile, indent=4, sort_keys=False)
    rcsID = ["turnew2", "goldsd3"]
    Tree = createCourseTree()
    print(Tree)
