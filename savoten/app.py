import datetime
import dateutil.parser
from flask import Flask, jsonify, abort, make_response, request, render_template
from savoten import domain

api = Flask(__name__)

events = []


@api.route('/api/v1/events/<string:event_id>', methods=['GET'])
def find_event_by_id(event_id):
    try:
        for event in events:
            if event.id == int(event_id):
                response = {
                    'data': {
                        'id': event.id,
                        'name': event.name,
                        'items': event.items,
                        'start': event.period.start,
                        'end': event.period.end,
                        'description': event.description,
                        'anonymous': event.anonymous,
                        'created_at': event.created_at,
                        'updated_at': event.updated_at,
                        'deleted_at': event.deleted_at
                    }
                }
                return make_response(jsonify(response), 200)
        # if event is not found, return status_code:200 and result:False.
        return make_response(jsonify({'data': {}}), 404)
    except Exception as e:
        error_message = 'get_event fail'
        api.logger.error('%s %s' % (error_message, e))
        response = {
            'error_message': error_message
        }
        return make_response(jsonify(response), 500)


@api.route('/api/v1/events', methods=['POST'])
def create_event():
    try:
        period_args = {
            # datetime.datetime parse
            'start': dateutil.parser.parse(request.json['start']),
            'end': dateutil.parser.parse(request.json['end']),
        }
        period = domain.Period(**period_args)

        event_args = {
            'name': request.json['name'],
            'period': period,
        }
        event_args['id'] = len(events) + 1
        event_args['items'] = []

        # non-required parameter keys
        event_option_keys = [
            'description',
            'anonymous',
            'created_at',
            'updated_at',
            'deleted_at'
        ]
        # set non-required parameter to event_args.
        for key in event_option_keys:
            if key in request.json:
                event_args[key] = request.json[key]

        event = domain.Event(**event_args)

        events.append(event)
    except Exception as e:
        error_message = 'create_event fail'
        api.logger.error('%s %s' % (error_message, e))
        response = {
            'error_message': error_message
        }
        return make_response(jsonify(response), 400)

    response = {
        'id': event.id,
        'name': event.name,
        'start': event.period.start,
        'end': event.period.end,
        'description': event.description
    }

    return make_response(jsonify(response), 201)


@api.route('/create_event', methods=['GET'])
def create_event_page():
    return render_template('create_event.html')


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8000)
