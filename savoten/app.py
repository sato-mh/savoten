import datetime
from flask import Flask, jsonify, abort, make_response
from savoten import domain

api = Flask(__name__)

@api.route('/events/<string:event_id>', methods=['GET'])
def get_event(event_id):
    try:
        start = datetime.datetime.now()
        end = start + datetime.timedelta(hours=1)
        args = {
            'name': event_id,
            'items': [],
            'period': domain.Period(start, end),
            'description': 'description for test'
        }
        event = domain.Event(**args)
    except:
        print ("except")
        abort(404)

    result = {
        "result":True,
        "data":{
            "event_id":event.id,
            "event_items":event.items,
            "period_start":event.period.start,
            "period_end": event.period.end,
            "description":event.description
            }
        }

    return make_response(jsonify(result))

@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8000)
