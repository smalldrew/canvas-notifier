import os
from dotenv import load_dotenv
import requests

load_dotenv()

CANVAS_API_TOKEN = os.getenv('CANVAS_API_TOKEN')  # Your Canvas API token
CANVAS_URL = 'https://canvas.instructure.com/api/v1'
HEADER = {'Authorization': f'Bearer {CANVAS_API_TOKEN}', }


def _get_user_id() -> int:  # this is not used but could be useful in the future
    """Queries Canvas for user id"""
    user_id_url = f'{CANVAS_URL}/users/self'
    response = requests.get(url=user_id_url, headers=HEADER)

    if response.status_code == 200:
        data = response.json()
        return data["id"]

    return -1


def get_course_list() -> list[dict]:
    """Returns a list of courses from the user"""
    courses_url = f'{CANVAS_URL}/courses'
    course_params = {
        'enrollment_type': 'student',
        'enrollment_state':'active',
    }
    course_list = []

    request = requests.get(url=courses_url, params=course_params, headers=HEADER)

    if request.status_code == 200:
        course_data = request.json()

        for course in course_data:
            curr_course_data = {
                'id': course['id'],
                'name': course['name'],
                'time_zone': course['time_zone'],

            }

            course_list.append(curr_course_data)

    return course_list


def unsubmitted_course_assignments(course: dict):
    """Gets the assignment due dates of a course"""
    course_due_date_url = f'{CANVAS_URL}/courses/{course["id"]}/assignments'
    assignment_params = {
        'include[]': 'submission',
        'bucket': 'upcoming',
    }

    request = requests.get(url=course_due_date_url, headers=HEADER, params=assignment_params)
    assignment_list = []

    if request.status_code == 200:
        data = request.json()
        for assignment in data:
            if assignment['due_at'] is None:
                continue

            # if assignment is already submitted
            if assignment['submission']['submitted_at']:

            curr_assignment_data = {
                'name' : assignment['name'],
                'points_possible': assignment['points_possible'],
                'due_at': assignment['due_at'],
            }
            assignment_list.append(curr_assignment_data)

    course['assignments'] = assignment_list
    return course


if __name__ == '__main__':
    user_courses = get_course_list()
    for curr_course in user_courses:
        print(unsubmitted_course_assignments(curr_course))
