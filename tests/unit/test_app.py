import json
import pytest
from savoten import app


@pytest.fixture(scope='class')
def test_app():
    uri = '/events'
    post_params = {
        "name": "test_name",
        "start": "2019-08-01 01:02:03.123456",
        "end": "2020-08-01 01:02:03.123456",
        "description": "test_desc"
    }
    test_app = app.api.test_client()
    response = test_app.post(uri, data=json.dumps(
        post_params), content_type='application/json')
    if response.status_code != 201:
        assert False
    return test_app


@pytest.mark.parametrize('uri, expect_status_code, expect_result', [
    ('/events/1', 200, True),
    ('/events/999', 200, False)
])
class TestGetEventClass():
    def test_get_event(self, test_app, uri, expect_status_code, expect_result):
        response = test_app.get(uri)
        assert (response.status_code == expect_status_code
                and response.json['result'] is expect_result)


@pytest.fixture(
    scope='function',
    params=[
        {
            # success case
            'uri': '/events',
            'post_params': {
                "name": "test_name",
                "start": "2019-08-01 01:02:03.123456",
                "end": "2019-08-02 01:02:03.123456",
                "description": "test_desc"
            },
            'expect': 201
        },
        {
            # fail case (missing post_params['name'])
            'uri': '/events',
            'post_params': {
                "start": "2019-08-01 01:02:03.123456",
                "end": "2019-08-02 01:02:03.123456",
                "description": "test_desc"
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
    post_params = post_event_test_case['post_params']
    test_app = app.api.test_client()
    response = test_app.post(uri, data=json.dumps(
        post_params), content_type='application/json')
    assert response.status_code == expect
