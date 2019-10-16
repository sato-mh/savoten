import dateutil.parser
from flask import jsonify, make_response, request
from flask.views import MethodView

from savoten import domain, repository
from savoten.logger import get_logger

logger = get_logger(__name__)

event_repository = repository.EventRepository()


class EventAPI(MethodView):

    def get(self, id):
        if id is None:
            return self._find_all()
        else:
            return self._find_by_id(id)

    def _find_all(self):
        events = event_repository.find_all().values()
        try:
            event_list = [{
                'id': event.id,
                'name': event.name,
                'start': event.period.start,
                'end': event.period.end,
                'description': event.description
            } for event in events]
            return make_response(jsonify({'events': event_list}), 200)
        except Exception as e:
            error_message = 'get_events fail'
            logger.error('%s %s' % (error_message, e))
            response = {'error_message': error_message}
            return make_response(jsonify(response), 500)

    def _find_by_id(self, id):
        try:
            event = event_repository.find_by_id(id)
            if event is None:
                return make_response(jsonify({'data': {}}), 404)
            else:
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
        except Exception as e:
            error_message = 'find_event_by_id fail'
            logger.error('%s %s' % (error_message, e))
            response = {'error_message': error_message}
            return make_response(jsonify(response), 500)

    def post(self):
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
            event_args['items'] = []

            # non-required parameter keys
            event_option_keys = [
                'description', 'anonymous', 'created_at', 'updated_at',
                'deleted_at'
            ]
            # set non-required parameter to event_args.
            for key in event_option_keys:
                if key in request.json:
                    event_args[key] = request.json[key]

            event = domain.Event(**event_args)

            event_repository.save(event)
        except Exception as e:
            error_message = 'create_event fail'
            logger.error('%s %s' % (error_message, e))
            response = {'error_message': error_message}
            return make_response(jsonify(response), 400)

        response = {
            'id': event.id,
            'name': event.name,
            'start': event.period.start,
            'end': event.period.end,
            'description': event.description
        }

        return make_response(jsonify(response), 201)
