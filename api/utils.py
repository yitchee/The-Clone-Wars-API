from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response

from api.models import ApiKey


def validate_request(request):
    result = {}
    try:
        origin = request.META['HTTP_ORIGIN']
    except:
        origin = ''
    
    if settings.DOMAIN_NAME not in origin:
        # Validate API key
        try:
            validate_apikey(request)
        except KeyError:
            result['error'] = 'Please provide an API key'
            result['status'] = 401
        except ObjectDoesNotExist:
            result['error'] = 'Invalid API key'
            result['status'] = 401
        except LimitExceededException:
            result['error'] = 'Daily limit exceeded.'
            result['status'] = 429
    
    return result


def validate_apikey(request):
    try:
        key = request.headers['X-API-KEY']
    except:
        raise(KeyError)
    
    # Check if API key is valid and within limit
    try:
        key = ApiKey.objects.get(key=key)
        limit = key.daily_limit
        if limit > 0:
            key.daily_limit = limit - 1
        else:
            raise(LimitExceededException)
        key.save()
    except LimitExceededException:
        raise(LimitExceededException)
    except:
        raise(ObjectDoesNotExist)


def set_options_response():
    response = Response()
    response['Allow'] = 'GET, OPTIONS, HEAD'
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'x-api-key'
    return response


class LimitExceededException(Exception):
    pass