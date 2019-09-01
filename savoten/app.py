from flask import Flask, jsonify, make_response

from savoten.handler import EventAPI, event_view

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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# register APIs
register_api(
    EventAPI,
    name='event_api',
    path='/api/v1/events',
)

# register views
app.register_blueprint(event_view)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
