import json
import pytest
from savoten import app


@pytest.fixture(scope='class')
def test_app():
    uri = '/api/v1/events'
    post_params = {
        "name": "test_name",
        "start": "2019-08-01 01:02:03.123456",
        "end": "2020-08-01 01:02:03.123456",
        "description": "test_desc"
    }
    test_app = app.api.test_client()
    response = test_app.post(uri, data=json.dumps(
        post_params), content_type='application/json')
    return test_app


@pytest.mark.parametrize('uri, expect_status_code', [
    ('/api/v1/events/1', 200),
    ('/api/v1/events/999', 404)
])
class TestFindEventById():
    def test_find_event_by_id(self, test_app, uri, expect_status_code):
        response = test_app.get(uri)
        assert (response.status_code == expect_status_code)


@pytest.fixture(
    scope='function',
    params=[
        {
            # success case
            'uri': '/api/v1/events',
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
            'uri': '/api/v1/events',
            'post_params': {
                "start": "2019-08-01 01:02:03.123456",
                "end": "2019-08-02 01:02:03.123456",
                "description": "test_desc"
            },
            'expect': 400
        }
    ]
)
def create_event_test_case(request):
    return request.param


def test_create_event(create_event_test_case):
    uri = create_event_test_case['uri']
    expect = create_event_test_case['expect']
    post_params = create_event_test_case['post_params']
    test_app = app.api.test_client()
    response = test_app.post(uri, data=json.dumps(
        post_params), content_type='application/json')
    assert response.status_code == expect
