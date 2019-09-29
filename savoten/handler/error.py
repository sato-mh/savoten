from flask import jsonify, make_response


def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def internal_error(error):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)
