import datetime
import json

import pytest
from flask import Flask, jsonify

from savoten.domain import Candidate, Event, EventItem, Period, User
from savoten.handler.util import DomainEncoder
from tests.util import get_public_vars

app = Flask(__name__)
# jsonifyで日本語処理を受け付ける設定
app.config['JSON_AS_ASCII'] = False

# jsonifyでdomainのclassを含むエンコードを行う設定
app.json_encoder = DomainEncoder

user_args = {
    'id': 1,
    'name': 'user_name',
    'email': 'user_email@example.com',
    'permission': 100
}
user = User(**user_args)
expected_user_dict = vars(user)

candidate_args = {'id': 1, 'user': user, 'description': 'candidate_description'}
candidate = Candidate(**candidate_args)
expected_candidate_dict = {
    'id': 1,
    'user': expected_user_dict,
    'description': 'candidate_description'
}

start = datetime.datetime.now()
end = start + datetime.timedelta(hours=1)
period_args = {'start': start, 'end': end}
period = Period(**period_args)
isoformatted_period = {'start': start.isoformat(), 'end': end.isoformat()}

event_item_args = {
    'id': 1,
    'name': 'event_item_name',
    'candidates': [candidate],
    'description': 'event_item_description'
}
event_item = EventItem(**event_item_args)
expected_event_item_dict = {
    'id': 1,
    'name': 'event_item_name',
    'candidates': [expected_candidate_dict],
    'seats': 1,
    'max_choice': 1,
    'min_choice': 1,
    'description': 'event_item_description'
}

event_args = {
    'id': 1,
    'name': 'event_name',
    'items': [event_item],
    'period': period,
    'description': 'event_description'
}
event = Event(**event_args)
expected_event_dict = {
    'id': 1,
    'name': 'event_name',
    'items': [expected_event_item_dict],
    'period': isoformatted_period,
    'description': 'event_description'
}

domains_objects = {
    'period': (period, isoformatted_period),
    'user': (user, expected_user_dict),
    'candidate': (candidate, expected_candidate_dict),
    'event_item': (event_item, expected_event_item_dict),
    'event': (event, expected_event_dict)
}


@pytest.mark.parametrize('domain_object, expected',
                         list(domains_objects.values()),
                         ids=list(domains_objects.keys()))
# jsonifyでdomainのオブジェクトをjson化するテスト
# savoten.handler.util.DomainEncoderクラスを予めjsonifyで使用する設定をして実行
def test_succeeds_when_jsonify_domains(domain_object, expected):
    with app.app_context():
        response = jsonify(domain_object)
    # json化したデータが正しいかの判定のためにjson.loadsしてdictに格納し直す
    parsed_response = json.loads(response.data)
    for key in expected:
        assert parsed_response[key] == expected[key]
