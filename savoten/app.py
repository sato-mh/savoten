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
    test_event_id = 1234
    try:
        if int(event_id) != test_event_id:
            raise Exception("event_id does not exist.")
        start = datetime.datetime.now()
        end = start + datetime.timedelta(hours=1)
        args = {
            'id': event_id,
            'name': 'get_event_stub event_name',
            'items': [],
            'period': domain.Period(start, end),
            'description': 'description for test'
        }
        event = domain.Event(**args)
    except:
        resp.status_code = api.status_codes.HTTP_404
        resp.media = {'result': False,
                      'error': 'Target event_id does not exist'}
        return

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
create_event
/eventにPOSTされたときのbodyからeventのパラメータを抽出
既存eventの総数を1インクリメントした値を新しいevent_idとしてセット
eventsに登録する
'''
@api.route('/events')
class Events():
    async def on_post(self, req, resp):
        try:
            request = await req.media()
            event_id = len(events) + 1
            start = datetime.datetime.now()
            end = start + datetime.timedelta(hours=24)
            args = {
                'id': event_id,
                'name': request['name'],
                'items': [],
                'period': domain.Period(start, end),
                'description': 'description for test'
            }
            event = domain.Event(**args)
            events[event_id] = event
        except:
            resp.status_code = api.status_codes.HTTP_400
            resp.media = {'result': False, 'error': 'create_event failed.'}
            return

        resp.status_code = api.status_codes.HTTP_201
        resp.media = {'result': True}


if __name__ == '__main__':
    api.run(address='0.0.0.0')
