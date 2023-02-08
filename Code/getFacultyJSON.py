import requests
import json
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # html = requests.get('https://faculty.rpi.edu/departments')
    html = requests.get('https://directory.rpi.edu/departments/')
    soup = BeautifulSoup(html.text, 'html.parser')

    # Get all the links for each department
    links = soup.find_all('a', href=True)

    # Create a dictionary to store the JSON data
    data = {}
    # Parse the links to get the faculty data
    for link in links:
        if link['href'].startswith('https://directory.rpi.edu/departments/'):
            departmentFaculty = {}
            html = requests.get(link['href'])
            soup = BeautifulSoup(html.text, 'html.parser')
            faculty = soup.find_all('tr')
            for person in faculty:
                if person.contents.__len__() < 8:
                    continue
                # print(person.contents[1].text.strip())
                # print(person.contents[3].text.strip())
                # print(person.contents[5].text.strip())
                # print(person.contents[7].text.strip())
                # break
                personDict = {}
                personDict['Name'] = person.contents[1].text.strip()
                personDict['Title'] = person.contents[3].text.strip()
                personDict['Email'] = person.contents[5].text.strip()
                personDict['Phone'] = person.contents[7].text.strip()
                departmentFaculty[personDict['Name']] = personDict
            data[link.text.strip()] = departmentFaculty
    # print(formatToJSON(data))




    # Write to JSON file
    with open('faculty.json', 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=False)
