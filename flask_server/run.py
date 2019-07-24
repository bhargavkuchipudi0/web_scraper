from flask import Flask
from task import task
from crontab import CronTab
import os

cron_tab = CronTab(user=True)

directory_path = os.getcwd()
path_to_cron_file = directory_path.split('/')[1: -1]
path_to_cron_file = 'python3' + '/' + '/'.join(path_to_cron_file) + '/scrapers/cron.py'


def start_cron_job():
    if len(cron_tab) < 1:
        job = cron_tab.new(
            command=path_to_cron_file, comment='1234')
        job.minute.every(1)
        job.enable()
        cron_tab.write()
        cron_tab.render()
        print('New cron job created with comment %s' % ('1234'))
    else:
        print('cron job already started with comment %s.' % ('1234'))


app = Flask(__name__)
app.register_blueprint(task)


@app.route('/')
def sys_ip():
    return 'server running on port 3500'


if __name__ == '__main__':
    print('Server started on port 3500')
    start_cron_job()
    app.run(port=3500, debug=True, use_reloader=False)
