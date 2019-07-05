import pytest
import json
from savoten import app


@pytest.fixture(scope='class')
def test_app():
    uri = '/events'
    data = {
        'name': 'test_event_data',
        'items': [],
        'description': 'TestGetEventClass preprocessing data'
    }
    test_app = app.api
    response = test_app.requests.post(uri, data)
    if response.status_code != 201:
        assert False
    return test_app


@pytest.mark.parametrize('uri, expect_status_code, expect_result', [
    ('/events/0', 200, True),
    ('/events/999', 200, False)
])
class TestGetEventClass():
    def test_get_event(self, test_app, uri, expect_status_code, expect_result):
        response = test_app.requests.get(uri)
        body = json.loads(response._content)
        assert (response.status_code == expect_status_code
                and body['result'] is expect_result)


@pytest.fixture(
    scope='function',
    params=[
        # 成功ケース(validation違反なし)
        {
            'uri': '/events',
            'data': {
                'name': 'create_event stub event_name',
                'items': [],
                'description': ''
            },
            'expect': 201
        },
        # 失敗ケース(nameの値が存在しない)
        {
            'uri': '/events',
            'data': {
                'name': None,
                'items': [],
                'description': ''
            },
            'expect': 400
        }
    ]
)
def post_event_test_case(request):
    return request.param


def test_post_event(post_event_test_case):
    uri = post_event_test_case['uri']
    expect = post_event_test_case['expect']
    data = post_event_test_case['data']
    test_app = app.api
    response = test_app.requests.post(uri, data)
    assert response.status_code == expect
