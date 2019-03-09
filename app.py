# update task keeps having error on 'done'
import json
from flask import Flask, request

app = Flask(__name__)
# package name

task_id_conunter = 2
tasks = {
    0: {
        'id':0,
        'description':'Laundry',
        'done': False
    },
    1:{
        'id':1,
        'description':'Homework',
        'done': False
    }
}

@app.route('/')
def root():
    return 'Hello world!'

@app.route('/tasks/')
def get_tasks():
    res = {'success':True, 'data':list(tasks.values())}
    return json.dumps(res), 200
# add task
@app.route('/tasks/', methods = ['POST'])
def create_task():
    global task_id_conunter
    post_body = json.loads(request.data)
    description = post_body['description']
    task = {
         'id': task_id_conunter,
         'description': description,
         'done': False
    }
    tasks[task_id_conunter] = task
    task_id_conunter += 1
    return json.dumps({'success':True,'data':task}),201
# localhost number task/10
# check if task is there
@app.route('/tasks/<int:task_id>/')
def get_task(task_id):
    if task_id in tasks:
        task = tasks[task_id]
        return json.dumps({'success':True,'data':task}),200
    if task_id not in tasks:
        return json.dumps({'success':False,'error':'Task not found!'}),404
# update task
@app.route('/tasks/<int:task_id>/', methods = ['POST'])
def update_task(task_id):
    if task_id in tasks:
        task = tasks[task_id]
        post_body = json.loads(request.data)
        task['description'] = post_body['description']
        # task['done'] = bool(post_body['done'])
        return json.dumps({'success':True,'data':task}),200
    return json.dumps({'success':False,'error':'Task not found!'}),404
# delete task
@app.route('/tasks/<int:task_id>/', methods = ['DELETE'])
def delete_task(task_id):
    if task_id in tasks:
        task = tasks[task_id]
        del tasks[task_id]
        return json.dumps({'success':True,'data':task}),200
    return json.dumps({'success':False,'error':'Task not found!'}),404
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
