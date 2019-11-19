from flask import Flask

from savoten.handler import EventAPI, event_view
from savoten.handler.error import internal_error, not_found

app = Flask(__name__)


def register_api(view, name, path, key='id', key_type='string'):
    view_func = view.as_view(name)
    app.add_url_rule(path,
                     defaults={key: None},
                     view_func=view_func,
                     methods=[
                         'GET',
                     ])
    app.add_url_rule(path, view_func=view_func, methods=[
        'POST',
    ])
    app.add_url_rule(f'{path}/<{key_type}:{key}>',
                     view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])


# register APIs
register_api(
    EventAPI,
    name='event_api',
    path='/api/v1/events',
)

# register views
app.register_blueprint(event_view)

# register error handler
app.register_error_handler(Exception, internal_error)
app.register_error_handler(404, not_found)
app.register_error_handler(500, internal_error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
