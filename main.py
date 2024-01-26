from dotenv import load_dotenv
import os
import requests
import json
from datetime import date

load_dotenv()

CANVAS_API_TOKEN = os.getenv('CANVAS_API_TOKEN')
CANVAS_URL = 'https://canvas.instructure.com/api/v1'

HEADER = {'Authorization': f'Bearer {CANVAS_API_TOKEN}', }

def get_user_id() -> int:
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


def get_assignment_due_dates(course: dict):
    """Gets the assignment due dates of a course"""
    course_due_date_url = f'{CANVAS_URL}/courses/{course["id"]}/effective_due_dates'

    request = requests.get(url=course_due_date_url, headers=HEADER)

    if request.status_code == 200:
        data = request.json()

    pass



# def planner_check():  # TODO: Get working (maybe)
#     user_id = get_user_id()
#     planner_url = f'{CANVAS_URL}/planner/items'
#
#     start = date(2024, 1, 1)
#     end = date(2024, 2, 24)
#
#     # planner_params = {
#     #     'start_date': start,
#     #     'end_date': end,
#     #     'observed_user_id': str(user_id),
#     # }
#     #
#     response = requests.get(url=planner_url, headers=HEADER)
#
#     print(response)
#
#     # Planner Object
#     # title - title of the planner object
#     # todo_date - date that should show up
#     # linked_object_type - assignment, quiz, etc.
#     # linked_object_html_url - planner url
#
#     if response.status_code == 200:
#          data = response.json()
#          print(data)


if __name__ == '__main__':
    # planner_check()
    pass
