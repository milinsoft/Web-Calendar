import datetime
import sys

from flask import Flask
from flask_restful import Resource, Api, reqparse, inputs, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy


TABLE_NAME: str = 'events'
NO_EVENTS_RESPONSE: dict = {"data": "There are no events for today!"}

app = Flask(__name__)
# SQLALCHEMY_DATABASE_URI is a DB configuration key
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{TABLE_NAME}.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)  # initialize database
api = Api(app)
db.create_all()  # save the table in the database


resource_fields = {
    "id": fields.Integer,
    "event": fields.String,
    "date": fields.String,
}


parser = reqparse.RequestParser()

parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! "
         "The correct format is YYYY-MM-DD!",
    required=True
)

parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)


class Event(db.Model):
    __tablename__ = TABLE_NAME

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)


class AllEventsResource(Resource):

    @staticmethod
    @marshal_with(resource_fields)
    def get():
        all_events = Event.query.all()
        if not all_events:
            return NO_EVENTS_RESPONSE

        return all_events

    @staticmethod
    def post():
        def add_to_db():
            event = Event(event=args['event'],
                          date=args['date'],
                          )
            db.session.add(event)
            db.session.commit()

        args = parser.parse_args()
        add_to_db()

        response = {
            "message": "The event has been added!",
            "event": args['event'],
            "date": str(args['date'].date())
        }

        return response


class EventResourceToday(AllEventsResource):

    @staticmethod
    @marshal_with(resource_fields)
    def get():
        todays_events = Event.query.filter(Event.date == datetime.date.today()).all()
        if not todays_events:
            return NO_EVENTS_RESPONSE
        return todays_events


api.add_resource(EventResourceToday, '/event/today')
api.add_resource(AllEventsResource, '/event')


# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
