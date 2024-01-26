from datetime import date
import canvas
from util.sms import send_text

BUFFER_MINUTES = 240  # minutes before assignment is due

def time_remaining():
    pass

def course_alert():
    send_text('hahaha')
    print(f'Text sent: bruh')

def check_course_due(ba):
    """Checks if the course"""


def main():
    print('Getting a list of courses...')
    course_list = canvas.get_course_list()

    if course_list:
        print('Received courses! \n')
    else:
        print('No courses found. \n')

    for course in course_list:
        print(f'Getting unsubmitted assignments for {course["name"]}...')
        canvas.unsubmitted_course_assignments(course)

        if not course["assignments"]:
            print('No assignments found.')

        for assignment in course["assignments"]:
            print(f'  - {assignment["name"]} | Due: {assignment["due_at"]}, Points: {assignment["points_possible"]}')

        print()
        # if check_course_due(course):
        #     course_alert(course)


    # print(course_list)

if __name__ == '__main__':
    main()
