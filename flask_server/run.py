from flask import Flask
from task import task

app = Flask(__name__)

app.register_blueprint(task)

@app.route('/')
def sys_ip():
    return 'server running on port 3500'

if __name__ == '__main__':
    print('Server started on port 3500')
    app.run(port=3500, debug=True)