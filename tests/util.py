import inspect


def get_public_vars(obj):

    def is_variable(obj_):
        return not hasattr(obj_, '__call__')

    def is_public(key):
        return not key.startswith('_')

    attrs = inspect.getmembers(obj, is_variable)
    return {k: v for k, v in attrs if is_public(k)}
