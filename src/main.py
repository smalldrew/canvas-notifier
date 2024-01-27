from datetime import datetime
import canvas
from util.sms import send_text
import pytz

# Warning Schedule: [1 day, 6 hours, 3 hours, 1 hour, 30 minutes, 10 minutes)
WARNING_SCHEDULE = [1440, 360, 180, 60, 30, 10]


def time_remaining(given_date) -> int:
    """Returns the time remaining for the given assignment in minutes"""
    current_time_utc = datetime.now(pytz.timezone('UTC'))  # Get current time in UTC format
    assignment_deadline = datetime.strptime(given_date, '%Y-%m-%dT%H:%M:%SZ')
    assignment_deadline = pytz.utc.localize(assignment_deadline)

    remaining_time = assignment_deadline - current_time_utc

    return int(remaining_time.total_seconds() / 60)


def days_hours_minutes_format(minutes) -> str:
    """Returns a format of Days, Hours, and Minutes"""
    days = minutes // (24 * 60)
    hours = (minutes % (24 * 60)) // 60
    remaining = minutes % 60

    return f'{days} Days, {hours} Hours, {remaining} Minutes'


def course_alert(assignment: dict) -> None:
    """Sends an alert text to the user"""
    assignment_due_in = days_hours_minutes_format(time_remaining(assignment["due_at"]))
    send_text('[CANVAS ALERT]\n'
              f'UNSUBMITTED: {assignment["name"]}\n'
              f'DUE IN: {assignment_due_in}\n'
              f'POINTS: {assignment["points_possible"]}')

    print(f'Sent Assignment Alert!')


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
            minutes_remaining = time_remaining(assignment["due_at"])
            time_left_formatted = days_hours_minutes_format(minutes_remaining)

            print(f'  - {assignment["name"]} | Due In: {time_left_formatted} | Points: {assignment["points_possible"]}')

            if minutes_remaining in WARNING_SCHEDULE:
                course_alert(assignment)

        print()


if __name__ == '__main__':
    main()
