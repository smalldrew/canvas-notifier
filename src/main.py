from datetime import datetime
from src import canvas
from util.sms import send_text
import pytz

BUFFER_MINUTES = 240  # minutes before assignment is due

def time_remaining(given_date, course_time_zone) -> float:
    """Returns the time remaining for the given assignment"""
    # (Canvas API returns time in UTC format)

    course_time_zone = pytz.timezone(course_time_zone)

    local_datetime = utc_datetime.replace(tzinfo = pytz.utc).astimezone(local_timezone)
    curr_time = datetime.now()
    assignment_deadline = datetime.strptime(given_date, '%Y-%m-%dT%H:%M:%SZ')


    time_diff = assignment_deadline - curr_time
    print(f'time diff: {time_diff}, assignment deadline: {assignment_deadline}')

    return time_diff.total_seconds() / 60

def days_hours_minutes_format(minutes):
    days = minutes // (24 * 60)
    hours = (minutes % (24 * 60)) // 60
    remaining = minutes % 60

    return f'{days} Days, {hours} Hours, {remaining} Minutes'

def course_alert(course):
    """Sends an alert text to """
    send_text('hahaha')
    print(f'Text sent: bruh')

def check_course_due(ba):
    """Checks if the course"""


def main():
    """Do a full check on Canvas assignments and send a text if necessary."""
    print('Getting a courses from Canvas...')
    course_list = canvas.get_course_list()

    if course_list:
        print('Courses found! \n')
    else:
        print('No courses found. \n')

    for course in course_list:
        print(f'Unsubmitted assignments for {course["name"]}:')
        canvas.unsubmitted_course_assignments(course)

        if not course["assignments"]:
            print('No assignments found.')

        for assignment in course["assignments"]:
            time_left = days_hours_minutes_format(int(time_remaining(assignment["due_at"])) )
            print(f'  - {assignment["name"]} | Due In: {time_left} | Points: {assignment["points_possible"]}')

        print()
        # if check_course_due(course):
        #     course_alert(course)


    # print(course_list)


if __name__ == '__main__':
    main()
