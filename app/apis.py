# from flask import make_response, jsonify, request
# from werkzeug.exceptions import abort
#
#
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)
#
# @app.route('/bucketlists/', methods=['POST', 'GET'])
# def bucketlists():
#     from app.models import BucketList
#     if request.method == "POST":
#         name = str(request.json.get('name', ''))
#         if name:
#             bucketlist = BucketList(name=name)
#             bucketlist.save()
#             response = jsonify({
#                 'id': bucketlist.id,
#                 'name': bucketlist.name,
#                 'date_created': bucketlist.date_created,
#                 'date_modified': bucketlist.date_modified
#             })
#             response.status_code = 201
#             return response
#     else:
#         # GET
#         bucketlists = BucketList.get_all()
#         results = []
#
#         for bucketlist in bucketlists:
#             obj = {
#                 'id': bucketlist.id,
#                 'name': bucketlist.name,
#                 'date_created': bucketlist.date_created,
#                 'date_modified': bucketlist.date_modified
#             }
#             results.append(obj)
#         response = jsonify(results)
#         response.status_code = 200
#         return response
#
# @app.route('/bucketlists/<id>', methods=['GET'])
# def fetch_bucket_by_id(id):
#     from app.models import BucketList
#     # print "incoming id: {}".format(id)
#     bucket = BucketList.fetch_by_id(id)
#     if bucket is not None:
#         obj = {
#             'id': bucket.id,
#             'name': bucket.name,
#             'date_created': bucket.date_created,
#             'date_modified': bucket.date_modified
#         }
#         response = jsonify(obj)
#         response.status_code = 200
#     else:
#         response = jsonify({'message': 'does not exists', 'status': 'failure'})
#         response.status_code = 404
#     return response
#
# @app.route('/v1/tasks', methods=['GET'])
# def get_tasks():
#     from app.models import Task
#     results = []
#     for task in Task.get_all():
#         obj = {
#             'id': task.id,
#             'title': task.title,
#             'description': task.description,
#         }
#         results.append(obj)
#     return jsonify({'tasks': results})
#
# @app.route('/v1/tasks/<int:task_id>', methods=['GET'])
# def get_task(task_id):
#     from app.models import Task
#     task = Task.fetch_by_id(task_id)
#     if task is None:
#         abort(404)
#     return jsonify({
#         'id': task.id,
#         'title': task.title,
#         'description': task.description,
#     })
#
# @app.route('/v1/tasks', methods=['POST'])
# def create_task():
#     from app.models import Task
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     task = Task(request.json['title'], request.json['description'])
#     task.save()
#     response = jsonify({
#         'id': task.id,
#         'title': task.title,
#         'description': task.description,
#     })
#     response.status_code = 201
#     return response
#
# @app.route('/v1/tasks/<int:task_id>', methods=['PUT'])
# def update_task(task_id):
#     from app.models import Task
#     task = Task.fetch_by_id(task_id)
#     if task is None:
#         abort(404)
#     if not request.json:
#         abort(400)
#     if 'title' in request.json and type(request.json['title']) != unicode:
#         abort(400)
#     if 'description' in request.json and type(request.json['description']) is not unicode:
#         abort(400)
#     if 'done' in request.json and type(request.json['done']) is not bool:
#         abort(400)
#     task.title = request.json.get('title', task.title)
#     task.description = request.json.get('description', task.description)
#     task.done = request.json.get('done', task.done)
#     task.save()
#     return jsonify({'task': {
#         'id': task.id,
#         'title': task.title,
#         'description': task.description,
#     }})
#
# @app.route('/v1/tasks/<int:task_id>', methods=['DELETE'])
# def delete_task(task_id):
#     from app.models import Task
#     task = Task.fetch_by_id(task_id)
#     if task is None:
#         abort(404)
#     task.delete()
#     return jsonify({'status': 'success', 'message': 'Task with id: {} deleted successfully!!'.format(task_id)})


class SomeObject(object):
    """
        Some object to test check output
    """

    def __init__(self, id, name, full_name):
        self.id = id
        self.name = name
        self.full_name = full_name

    def __repr__(self):
        return "SomeObject id {}, name {}, fullname: {}".format(self.id, self.name, self.full_name)
