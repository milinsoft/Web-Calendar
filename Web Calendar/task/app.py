import datetime
import sys

from flask import Flask, abort, render_template, Response, request
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

resource_fields = {
    "message": fields.String,
    "id": fields.Integer,
    "event": fields.String,
    "date": fields.String,
}


def page_not_found(e):
    return render_template('404.html'), 404


class Event(db.Model):
    __tablename__ = TABLE_NAME

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)


db.create_all()  # save the table in the database


class MainPageResource(Resource):

    @staticmethod
    def get():
        return Response(render_template('index.html'), mimetype='text/html')


class AllEventsResource(Resource):

    @staticmethod
    @marshal_with(resource_fields)
    def get():
        start = request.args.get('start_time')
        end = request.args.get('end_time')
        if all((start, end)):
            range_events = Event.query.filter(Event.date.between(start, end)).all()
            return range_events

        all_events = Event.query.all()

        if not all_events:
            return NO_EVENTS_RESPONSE

        return all_events

    @staticmethod
    @marshal_with(resource_fields)
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
        todays_events = Event.query.filter(Event.date == datetime.datetime.today().date()).all()
        if not todays_events:
            return NO_EVENTS_RESPONSE
        return todays_events


class EventByID(Resource):

    @staticmethod
    @marshal_with(resource_fields)
    def get(event_id):
        event = Event.query.filter(Event.id == event_id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        return event

    @staticmethod
    @marshal_with(resource_fields)
    def delete(event_id):

        event = Event.query.filter(Event.id == event_id).first()
        if not event:
            return abort(404, "The event doesn't exist!")
        db.session.delete(event)
        db.session.commit()
        return {"message": "The event has been deleted!"}


api.add_resource(EventResourceToday, '/event/today')
api.add_resource(EventByID, '/event/<int:event_id>')
api.add_resource(AllEventsResource, '/event')
api.add_resource(MainPageResource, '/')
app.register_error_handler(404, page_not_found)


# do not change the way you run the program
if __name__ == '__main__':

    def parse_all():
        parser.add_argument(
            'date', type=inputs.date,
            help="The event date with the correct format is required! "
                 "The correct format is YYYY-MM-DD!",
            required=True
        )

        parser.add_argument(
            'event', type=str,
            help="The event name is required!",
            required=True
        )

        parser.add_argument(
            'start_time', type=inputs.date,
            help="Start event date is required!"
                 "The correct format is YYYY-MM-DD!",
            required=False
        )

        parser.add_argument(
            'end_time', type=inputs.date,
            help="End event date is required!"
                 "The correct format is YYYY-MM-DD!",
            required=False,
        )

    parser = reqparse.RequestParser()
    parse_all()

    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
