import getAllCourseToJSON
import LoadJSONWithRCS
import getAllFacultyToJSON
import requests

# link = https://sis.rpi.edu/rss/bwckschd.p_disp_listcrse?term_in=
# 202301&subj_in=CSCI&crse_in=2961&crn_in=80260

# RCOS.html = https://sis.rpi.edu/rss/bwckschd.p_disp_listcrse?
# term_in=202301&subj_in=CSCI&crse_in=2961&crn_in=80260

# term_in=202301&

# term_in=202301&
# spring=01
# fall=09
# arch=05
# winter=12

# subj_in=CSCI&
# crse_in=2961&
# crn_in=80260


def main():
    session = requests.Session()
    getAllCourseToJSON.CreateCoursesJSON()
    print("Courses.json created")
    LoadJSONWithRCS.FillJSONWithRCSIDs(session)
    print("Courses.json filled with RCSIDs")
    getAllFacultyToJSON.FacultyToJSON(session)
    print("Faculty.json created")


if __name__ == "__main__":
    main()
    print("Done")
