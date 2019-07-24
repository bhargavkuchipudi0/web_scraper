from flask import Blueprint, request, json, jsonify

import os
import sys
sys.path.insert(0, os.path.abspath(".."))

from scrapers.scrap import Scraper
from database import mongo_db

task = Blueprint('task_apis', __name__, url_prefix='/ws')


@task.route('/user', methods=['POST'])
def add_user():
    response = mongo_db.save_user(json.loads(request.data))
    res = jsonify(response)
    res.status_code = response['status_code']
    return res


@task.route('/user', methods=['GET'])
def get_user():
    response = mongo_db.get_user_by_id(request.args['_id'])
    res = jsonify(response)
    res.status_code = response['status_code']
    return res

@task.route('/user', methods=['PUT'])
def update_user():
    response = mongo_db.update_user_by_id(json.loads(request.data))
    res = jsonify(response)
    res.status_code = response['status_code']
    return res

@task.route('/task', methods=['POST'])
def create_task():
    body = json.loads(request.data)
    scrap_data = Scraper(body['url'])
    scrap_data = scrap_data.get_url_from_user()
    body.update(scrap_data)
    task_response = mongo_db.create_task(body)
    response = jsonify(task_response)
    response.status_code = task_response['status_code']
    return response
    
@task.route('/user/tasks', methods=['GET'])
def get_task_of_user():
    tasks = mongo_db.get_tasks_of_user(request.args['_id'])
    response = jsonify(tasks)
    response.status_code = tasks['status_code']
    return response
