import logging

from flask import jsonify, request, Flask, abort, make_response, logging
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

# local import
from app.apis import SomeObject
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()
# https://flask-httpauth.readthedocs.io/en/latest/
# http://flask.pocoo.org/snippets/8/
auth = HTTPBasicAuth()


def _configure_logging(app):
    # set logger
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s: [in %(pathname)s:%(lineno)d] \t%(message)s')
    ch.setFormatter(formatter)
    app.logger.removeHandler('debug')
    for hdlr in app.logger.handlers:
        app.logger.removeHandler(hdlr)

    app.logger.addHandler(ch)


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    _configure_logging(app)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    @app.route('/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
        from app.models import BucketList
        app.logger.info("inside get bucket lists");
        if request.method == "POST":
            name = str(request.json.get('name', ''))
            if name:
                bucketlist = BucketList(name=name)
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                })
                response.status_code = 201
                return response
        else:
            # GET
            bucketlists = BucketList.get_all()
            results = []

            for bucketlist in bucketlists:
                obj = {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/bucketlists/<id>', methods=['GET'])
    def fetch_bucket_by_id(id):
        from app.models import BucketList
        # print "incoming id: {}".format(id)
        bucket = BucketList.fetch_by_id(id)
        if bucket is not None:
            obj = {
                'id': bucket.id,
                'name': bucket.name,
                'date_created': bucket.date_created,
                'date_modified': bucket.date_modified
            }
            response = jsonify(obj)
            response.status_code = 200
        else:
            response = jsonify({'message': 'does not exists', 'status': 'failure'})
            response.status_code = 404
        return response

    @app.route('/v1/tasks', methods=['GET'])
    def get_tasks():
        from app.models import Task
        results = []
        for task in Task.get_all():
            obj = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
            }
            results.append(obj)
        return jsonify({'tasks': results})

    @app.route('/v1/tasks/<int:task_id>', methods=['GET'])
    def get_task(task_id):
        from app.models import Task
        task = Task.fetch_by_id(task_id)
        if task is None:
            abort(404)
        return jsonify({
            'id': task.id,
            'title': task.title,
            'description': task.description,
        })

    @app.route('/v1/tasks', methods=['POST'])
    def create_task():
        from app.models import Task
        from app.forms import TaskForm
        # if not request.json or not 'title' in request.json:
        #     abort(400)
        # task = Task(request.json['title'], request.json['description'])
        task_form = TaskForm(**request.json)
        if task_form.validate():
            task = task_form.get_task()
            task.save()
            response = jsonify({
                'id': task.id,
                'title': task.title,
                'description': task.description,
            })
            response.status_code = 201
        else:
            response = jsonify({'errors': task_form.errors})
            response.status_code = 500

        return response

    @app.route('/v1/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        from app.models import Task
        task = Task.fetch_by_id(task_id)
        if task is None:
            abort(404)
        if not request.json:
            abort(400)
        if 'title' in request.json and type(request.json['title']) != unicode:
            abort(400)
        if 'description' in request.json and type(request.json['description']) is not unicode:
            abort(400)
        if 'done' in request.json and type(request.json['done']) is not bool:
            abort(400)
        task.title = request.json.get('title', task.title)
        task.description = request.json.get('description', task.description)
        task.done = request.json.get('done', task.done)
        task.save()
        return jsonify({'task': {
            'id': task.id,
            'title': task.title,
            'description': task.description,
        }})

    @app.route('/v1/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        from app.models import Task
        task = Task.fetch_by_id(task_id)
        if task is None:
            abort(404)
        task.delete()
        return jsonify({'status': 'success', 'message': 'Task with id: {} deleted successfully!!'.format(task_id)})

    @app.route('/v1/register/', methods=['POST'], strict_slashes=False)
    def register_user():
        from forms import RegistrationForm
        form = RegistrationForm(**request.json)
        if form.validate():
            return jsonify({'form_data': form.data, 'form_attributes': form.creator}), 200
        return jsonify(form.errors), 401

    @app.route('/v1/login/', methods=['POST'], strict_slashes=False)
    def login():
        from forms import RegistrationForm, LoginForm
        form = LoginForm(**request.json)
        if form.validate():
            return jsonify(form.user), 200
        return jsonify(form.errors), 401

    @app.route('/index')
    @auth.login_required
    def index():
        return "Hello, %s!" % auth.username()

    @app.route('/some')
    def some():
        some = SomeObject('x', 'y', 'z')
        return jsonify(some.__dict__), 200

    return app