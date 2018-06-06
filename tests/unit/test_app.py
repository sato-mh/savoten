import pytest
from savoten import app


@pytest.fixture(
    scope='function',
    params=[
        {
            'uri': '/events/1234',
            'expect': 200
        },
        {
            'uri': '/events/',
            'expect': 404
        }
    ]
)
def get_event_test_case(request):
    return request.param


def test_get_event(get_event_test_case):
    uri = get_event_test_case['uri']
    expect = get_event_test_case['expect']
    test_app = app.api.test_client()
    response = test_app.get(uri)
    assert response.status_code == expect
