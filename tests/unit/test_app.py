import pytest
from savoten import app


@pytest.fixture(
    scope='function',
    params=[
        # 成功ケース(IDが存在する)
        {
            'uri': '/events/1234',
            'expect': 200
        },
        # 失敗ケース(IDが存在しない)
        {
            'uri': '/events/9999',
            'expect': 404
        }
    ]
)
def get_event_test_case(request):
    return request.param


def test_get_event(get_event_test_case):
    uri = get_event_test_case['uri']
    expect = get_event_test_case['expect']
    test_app = app.api
    response = test_app.requests.get(uri)
    assert response.status_code == expect


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
