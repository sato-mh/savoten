import datetime
import responder
from savoten import domain

api = responder.API()

events = []


@api.route('/events/{event_id}')
def get_event(req, resp, *, event_id):
    # stub動作
    # global変数のeventsに登録のあるeventをidでsearchして結果を返す
    # 見つからなかったときは200でresult:Falseを返す
    try:
        for event in events:
            if event.id == int(event_id):
                body = {
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
                break
        else:
            body = {'result': False}
        resp.media = body
    except:
        resp.status_code = api.status_codes.HTTP_500
        resp.media = {
            'result': False,
            'error': 'get_event error'
        }


@api.route('/events')
class Events():
    async def on_post(self, req, resp):
        try:
            # stub用にダミーパラメータ生成を
            # request['name']のみ抽出してglobal変数のeventsにevent登録
            request = await req.media()
            event_id = len(events)
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
            events.append(event)
            resp.status_code = api.status_codes.HTTP_201
            resp.media = {'result': True}
        except:
            resp.status_code = api.status_codes.HTTP_400
            resp.media = {'result': False, 'error': 'create_event failed.'}


if __name__ == '__main__':
    api.run(address='0.0.0.0', port=8000)
