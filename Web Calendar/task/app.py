import sys

from flask import Flask
from flask_restful import Api, Resource, reqparse, inputs

app = Flask(__name__)

# write your code here
api = Api(app)


class EventResource(Resource):
    @staticmethod
    def get():
        return {"data": "There are no events for today!"}

    @staticmethod
    def post():
        args = parser.parse_args()
        response = {
            "message": "The event has been added!",
            "event": args['event'],
            "date": str(args['date'].date())
        }

        return response


def set_arguments():
    parser.add_argument(
        'date',
        type=inputs.date,
        help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
        required=True
    )

    parser.add_argument(
        'event',
        type=str,
        help="The event name is required!",
        required=True
    )


# do not change the way you run the program
if __name__ == '__main__':
    parser = reqparse.RequestParser()
    set_arguments()
    api.add_resource(EventResource, '/event/')

    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
