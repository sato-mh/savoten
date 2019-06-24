import datetime
import responder
from savoten import domain

api = responder.API()

events = {}

'''
get_event
GETされたときのuriからevent_idを抽出
DBに問い合わせ、event.idと対応するeventがあれば返す
なければ404を返す
'''
@api.route('/events/{event_id}')
def get_event(req, resp, *, event_id):

    # stubの動作
    # stub応答のためダミーパラメータでeventオブジェクトを生成
    try:
        start = datetime.datetime.now()
        end = start + datetime.timedelta(hours=1)
        args = {
            'id': event_id,
            'name': 'test event_name',
            'items': [],
            'period': domain.Period(start, end),
            'description': 'description for test'
        }
        event = domain.Event(**args)
    except Exception as e:
        print('exception: %s', e)
        resp.status_code = api.status_codes.HTTP_404
        resp.media = {'error': 'Not found'}

    # レスポンスに使うdictを生成
    result = {
        'result': True,
        'data': {
            'event_id': event.id,
            'event_name': event.name,
            'event_items': event.items,
            'period_start': event.period.start.strftime('%Y-%m-%d %H:%M:%S'),
            'period_end': event.period.end.strftime('%Y-%m-%d %H:%M:%S'),
            'description': event.description
        }
    }
    # レスポンス
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
'''

if __name__ == '__main__':
    api.run(address='0.0.0.0')
