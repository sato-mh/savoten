import datetime
import json

import pytest

from savoten import domain
from savoten.app import app
from savoten.handler.event_api import event_repository

start = datetime.datetime.now()
end = start + datetime.timedelta(hours=1)
period_args = {'start': start, 'end': end}
period = domain.Period(**period_args)
event_args = {
    'name': 'test_name',
    'period': period,
    'description': 'test_desc',
    'items': []
}


class TestGetEvents:

    def setup_method(self):
        self.client = app.test_client()

    @pytest.mark.parametrize('uri, expect_status_code',
                             [('/api/v1/events', 200)])
    def test_success_case(self, uri, expect_status_code):
        response = self.client.get(uri)
        assert (response.status_code == expect_status_code)


class TestFindEventById:

    def setup_method(self):
        self.client = app.test_client()
        event = domain.Event(**event_args, id=1)
        event_repository.save(event)

    @pytest.mark.parametrize(
        'uri, expect_status_code',
        [
            ('/api/v1/events/1', 200),  # success case
            ('/api/v1/events/999', 404)  # fail case (Target ID does not exist.)
        ])
    def test_find_event_by_id(self, uri, expect_status_code):
        response = self.client.get(uri)
        assert (response.status_code == expect_status_code)


class TestCreateEvent:

    def setup_method(self):
        self.client = app.test_client()

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
        ])
    def test_case(self, request):
        return request.param

    def test_create_event(self, test_case):
        uri = test_case['uri']
        expect = test_case['expect']
        post_params = test_case['post_params']
        response = self.client.post(uri,
                                    data=json.dumps(post_params),
                                    content_type='application/json')
        assert response.status_code == expect
