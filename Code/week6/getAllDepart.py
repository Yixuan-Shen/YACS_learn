# -*- coding: utf-8 -*-
# This is a temporary helper script to get all the departments
# Before we have a better way to get all the departments
# it will dump all the departments to a json file called Departments.json
import json


def getDepartmentsFromFile(Filename: str) -> list:
    # get all departments
    # return a list of departments
    ret = []
    with open(Filename, 'r') as infile:
        data = json.load(infile)
        infile.close()
        for semester in data:
            for department in data[semester]:
                ret.append(department)

    return ret


if __name__ == "__main__":
    Departments = getDepartmentsFromFile('Courses.json')
    print(Departments)
    with open('Departments.json', 'w') as outfile:
        json.dump(Departments, outfile, indent=4, sort_keys=True)
        outfile.close()
