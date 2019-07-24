from mongoengine import *
from .schema import Users, Tasks
import json
import datetime

connect('web_scraper', host='localhost', port=27017)


def save_user(user_data):
    new_user = Users(**user_data)
    response = None
    try:
        new_user.save()
        response = {'status_code': 200, 'message': 'user registered'}
    except NotUniqueError:
        response = {'status_code': 409,
                    'message': 'email id already registered'}
    except:
        response = {'status_code': 500,
                    'message': 'error while storing user in db'}
    return response


def get_user_by_id(user_id):
    user = None
    try:
        user = Users.objects(id=user_id).first().to_json()
        print(user)
        user = {
            'status_code': 200,
            'user': json.loads(user)
        }
    except:
        user = {
            'status_code': 500,
            'message': 'server error'
        }
    return user


def update_user_by_id(user_data):
    user_id = user_data['_id']['$oid']
    user_data.pop('_id', None)
    user_data['created_on'] = datetime.datetime.now
    print(user_data)
    user = None
    try:
        user = Users.objects(id=user_id).update_one(**user_data)
        if user:
            user = {
                'status_code': 200,
                'message': 'user updated successfully'
            }
        else:
            user = {
                'status_code': 500,
                'message': 'error updating user details'
            }
    except:
        user = {
            'status_code': 500,
            'message': 'error updating user details'
        }
    return user

def create_task(task_data):
    task = Tasks(**task_data)
    try:
        task = task.save()
        task = {
            'status_code': 200,
            'message': 'task created successfully'
        }
    except:
        task = {
            'status_code': 500,
            'message': 'error in creating the task'
        }
    return task
        
def get_tasks_of_user(user_id):
    try:
        tasks = Tasks.objects(user_id=user_id).to_json()
        if len(tasks) == 0:
            tasks = {
                status_code: 404,
                message: 'no tasks found'
            }
        else:
            tasks = {
                'status_code': 200,
                'tasks': json.loads(tasks)
            }
    except:
        tasks = {
            'status_code': 500,
            'message': 'server error'
        }
    return tasks