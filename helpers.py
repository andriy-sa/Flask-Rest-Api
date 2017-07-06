from flask import request
import random, string
from jwt import InvalidTokenError
from flask_jwt import JWT, JWTError

jwt = JWT()


def int_from_request(field, default):
    try:
        result = int(request.args.get(field, default))
    except:
        result = default

    return result


def float_from_request(field, default):
    try:
        result = float(request.args.get(field, default))
    except Exception:
        result = default

    return result

def bool_from_request(field, default):
    try:
        result = bool(int(request.args.get(field, default)))
    except Exception:
        result = default

    return result


def prepare_sorting_params(sort_list, default):
    sort = request.args.get('sort', default)
    reverse = request.args.get('reverse', 'DESC')

    if reverse != 'DESC' and reverse != 'ASC':
        reverse = 'DESC'

    if sort not in sort_list:
        sort = default

    return sort, reverse


def str_random(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def get_jwt_user():
    try:
        token = jwt.request_callback()
        payload = jwt.jwt_decode_callback(token)
        user = jwt.identity_callback(payload)
    except InvalidTokenError:
        user = None
    except JWTError:
        user = None

    return user
