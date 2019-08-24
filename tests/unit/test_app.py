import datetime
import json
import pytest
from savoten import app, domain


@pytest.fixture(
    scope='function',
    params=[
        {
            'uri': '/api/v1/events',
            'expect': 200
        }
    ]
)
def get_events_test_case(request):
    return request.param


class TestGetEvents:
    def setup_class(self):
        uri = '/api/v1/events'
        start = datetime.datetime.now()
        end = start + datetime.timedelta(hours=1)
        period_args = {
            'start': start,
            'end': end
        }
        period = domain.Period(**period_args)
        event_args = {
            'id': 1,
            'name': 'test_name',
            'period': period,
            'description': 'test_desc',
            'items': []
        }
        event = domain.Event(**event_args)
        app.events.append(event)

    def teardown_class(self):
        app.events.clear()

    def test_get_events(self, get_events_test_case):
        uri = get_events_test_case['uri']
        expect_status_code = get_events_test_case['expect']
        test_app = app.api.test_client()
        response = test_app.get(uri)
        assert (response.status_code == expect_status_code)


@pytest.fixture(
    scope='function',
    params=[
        {
            # success case
            'uri': '/api/v1/events/1',
            'expect': 200
        },
        {
            # fail case (Target ID does not exist.)
            'uri': '/api/v1/events/999',
            'expect': 404
        }
    ]
)
def find_event_by_id_test_case(request):
    return request.param


class TestFindEventById:
    def setup_class(self):
        uri = '/api/v1/events'
        start = datetime.datetime.now()
        end = start + datetime.timedelta(hours=1)
        period_args = {
            'start': start,
            'end': end
        }
        period = domain.Period(**period_args)
        event_args = {
            'id': 1,
            'name': 'test_name',
            'period': period,
            'description': 'test_desc',
            'items': []
        }
        event = domain.Event(**event_args)
        app.events.append(event)

    def teardown_class(self):
        app.events.clear()

    def test_find_event_by_id(self, find_event_by_id_test_case):
        uri = find_event_by_id_test_case['uri']
        expect_status_code = find_event_by_id_test_case['expect']
        test_app = app.api.test_client()
        response = test_app.get(uri)
        assert (response.status_code == expect_status_code)


@pytest.fixture(
    scope='function',
    params=[
        {
            # success case
            'uri': '/api/v1/events',
            'post_params': {
                'name': 'test_name',
                'start': '2019-08-01 01:02:03.123456',
                'end': '2019-08-02 01:02:03.123456',
                'description': 'test_desc'
            },
            'expect': 201
        },
        {
            # fail case (missing post_params['name'])
            'uri': '/api/v1/events',
            'post_params': {
                'start': '2019-08-01 01:02:03.123456',
                'end': '2019-08-02 01:02:03.123456',
                'description': 'test_desc'
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
