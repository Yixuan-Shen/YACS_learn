# -*- coding: utf-8 -*-
import getAllCourseToJSON
import LoadJSONWithRCS
import getAllFacultyToJSON
import requests


def main():
    session = requests.Session()
    getAllCourseToJSON.CreateCoursesJSON(session)
    print("Courses.json created")
    AllFaculty = LoadJSONWithRCS.FillJSONWithRCSIDs(session)
    print("Courses.json filled with RCSIDs")
    getAllFacultyToJSON.FacultyToJSON(AllFaculty, session)
    print("Faculty.json created")


if __name__ == "__main__":
    # TODO: Add more options and command line arguments support
    main()
    print("Done")
