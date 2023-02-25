import getAllCourseToJSON
import LoadJSONWithRCS
import getAllFacultyToJSON

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
    getAllCourseToJSON.CreateCoursesJSON()
    LoadJSONWithRCS.FillJSONWithRCSIDs()
    getAllFacultyToJSON.FacultyToJSON()


if __name__ == "__main__":
    main()
    print("Done")
