import sys

from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)

# write your code here
api = Api(app)


class HellowWorldResource(Resource):
    @staticmethod
    def get():
        return {"message": "Hello from the REST API!"}


class EventResource(Resource):
    @staticmethod
    def get():
        return {"data": "There are no events for today!"}


# do not change the way you run the program
if __name__ == '__main__':
    api.add_resource(HellowWorldResource, '/hello')
    api.add_resource(EventResource, '/event/today')
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
