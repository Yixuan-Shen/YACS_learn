import requests
import json
from bs4 import BeautifulSoup

# example link:
# https://sis.rpi.edu/rss/bwckschd.p_disp_listcrse?
# term_in=202301&amp;subj_in=CSCI&amp;crse_in=1100&amp;crn_in=76156


def praseSearchResult(file) -> dict:
    courseTree = dict()
    soup = BeautifulSoup(file, 'html.parser')
    links = getAllLink(soup)
    for link in links:
        course = link.split('?')[1]
        parts = course.split('&')
        parts[0] = parts[0].split('=')[1]
        parts[1] = parts[1].split('=')[1]
        parts[2] = parts[2].split('=')[1]
        parts[3] = parts[3].split('=')[1]
        if parts[0] not in courseTree:
            courseTree[parts[0]] = dict()
        if parts[1] not in courseTree[parts[0]]:
            courseTree[parts[0]][parts[1]] = dict()
        if parts[2] not in courseTree[parts[0]][parts[1]]:
            courseTree[parts[0]][parts[1]][parts[2]] = dict()
        if parts[3] not in courseTree[parts[0]][parts[1]][parts[2]]:
            courseTree[parts[0]][parts[1]][parts[2]][parts[3]] = []
        # courseTree[parts[0]][parts[1]][parts[2]][parts[3]] = []
    return courseTree


def getAllLink(soup) -> list:
    rawLinks = soup.find_all('a', href=True)
    returnLinks = []
    for link in rawLinks:
        if link['href'].startswith('https://sis.rpi.edu/rss/bwckschd.p_disp_listcrse?term_in='):
            returnLinks.append(link['href'])
    return returnLinks


if __name__ == "__main__":
    # html = requests(link)
    html = open('Search_Results.html', 'r')
    courseTree = praseSearchResult(html)

    # # Write to JSON file
    with open('Courses.json', 'w') as outfile:
        json.dump(courseTree, outfile, indent=4, sort_keys=False)