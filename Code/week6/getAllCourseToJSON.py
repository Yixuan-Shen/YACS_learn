# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup


def praseSearchResult(filename: str) -> dict:
    '''
    from the search result, save all the courses to dict tree
    with the structure of 
    dict[semester][department][course][crn] = [facultyRCSIDs]
    '''
    courseTree = dict()
    html = open(filename, 'r')
    soup = BeautifulSoup(html, 'html.parser')
    links = getAllLink(soup)
    html.close()

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
    return courseTree


def getAllLink(soup: BeautifulSoup) -> list:
    '''Helper function to get all the links from the soup'''
    rawLinks = soup.find_all('a', href=True)
    returnLinks = []
    for link in rawLinks:
        # If HTML was saved on Windows Firefox, the link will be shortened as
        # /rss/bwckschd.p_disp_listcrse?term_in=
        # Therefore I use a plugin to save the HTML as a single file
        # called "SingleFile"
        if link['href'].startswith('https://sis.rpi.edu/rss/bwckschd.p_disp_listcrse?term_in='):
            returnLinks.append(link['href'])
    return returnLinks


def CreateCoursesJSON(filename: str = '2023Spring.html'):
    '''Main function to parse data and create the JSON file'''
    # This prosess is totally offline for now
    # TODO: find the online link which can get same result
    # In that way, we can automate the process at a scheduled time
    courseTree = praseSearchResult(filename)

    with open('Courses.json', 'w') as outfile:
        json.dump(courseTree, outfile, indent=4, sort_keys=False)


if __name__ == "__main__":
    # This code can always run independently
    CreateCoursesJSON()
