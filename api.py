import json

from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

global global_int
global global_bool
global global_str
global_int = 1
global_bool = False
global_str = ''

# app name
@app.errorhandler(404)
def not_found(error):
    json_404 = '''
{
    "Error": {
        "simple": "''' + request.url + '''",
        "detailed": "''' + request.base_url + '''"
    }
}
'''
    return json_404, 404, {'Content-Type': 'application/json; charset=utf-8'}

@app.errorhandler(405)
def method_not_allowed(e):
    return {'error': 405}, 405

@app.route('/', methods=HTTP_METHODS)
def index():
    return { 'message': "Hello, World!" }

@app.route('/post', methods=['POST'])
def generic_post_function():
    if not 'some_password' in request.get_json():
        return { 'message': "You forgot the password." }, 401
    return request.get_json()

@app.route('/put', methods=['PUT'])
def generic_put_function():
    if 'some_int' in request.get_json():
        if not isinstance(request.get_json()['some_int'], int):
            return { 'message': "\"some_int\" is not an integer." }, 400
        global global_int
        global_int = request.get_json()['some_int']
    if 'some_bool' in request.get_json():
        if not isinstance(request.get_json()['some_bool'], bool):
            return { 'message': "\"some_bool\" is not an integer." }, 400
        global global_bool
        global_bool = request.get_json()['some_bool']
    if 'some_str' in request.get_json():
        if not isinstance(request.get_json()['some_str'], str):
            return { 'message': "\"some_str\" is not an integer." }, 400
        global global_str
        global_str = request.get_json()['some_str']
    return { 'Success': True }, 200

@app.route('/get', methods=['GET'])
def generic_get_function():
    global global_int
    global global_bool
    global global_str
    if global_str:
        bool_str = 'true'
    else:
        bool_str = 'false'
    json_resp = '''
{
    "int": ''' + str(global_int) + ''',
    "bool": ''' + bool_str + ''',
    "string": "''' + str(global_str) + '''"
}
'''
    return json_resp, 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='localhost',port='4000', debug=True)