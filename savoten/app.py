import datetime
import responder
from savoten import domain

api = responder.API()

events = {}


@api.route('/events/{event_id}')
def get_event(req, resp, *, event_id):
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
        resp.status_code = api.status_codes.HTTP_404

    result = {
        'result': True,
        'data': {
            'event_id': event.id,
            'event_items': event.items,
            'period_start': event.period.start,
            'period_end': event.period.end,
            'description': event.description
        }
    }
    resp.media = result


'''
@api.route('/events', methods=['POST'])
def create_event():

    print(events)
    event_id = len(events) + 1
    start = datetime.datetime.now()
    end = start + datetime.timedelta(hours=24)

    args = {
        'name': event_id,
        'items': [],
        'period': domain.Period(start, end),
        'description': 'description for test'
    }
    event = domain.Event(**args)

    events[event_id] = event

    return make_response(f'create event{vars(event)})!', 201)


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8000)
'''
