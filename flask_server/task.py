from flask import Blueprint, request, json, jsonify

import os
import sys
sys.path.insert(0, os.path.abspath(".."))
from scrapers.scrap import Scraper

task = Blueprint('task_apis', __name__, url_prefix='/task')


@task.route('/test_url', methods=['POST'])
def test_url():
    body = json.loads(request.data)
    scrap = Scraper(body['url'])
    res = scrap.get_url_from_user()
    print(res)
    res = jsonify(res)
    res.status_code = 200
    return res


@task.route('/test_url', methods=['GET'])
def get_testing_url():
    print(request.args['url'])
    return 'URL'
