import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from galtrace.libs import crawler
from galtrace.libs.core.models import Order, PHASES


def ajaxView(f):
    '''
    This decorator serialize returning object to JSON.
    All exceptions will be catched and serialized.
    For the contrast to Django, this decorator must be the most inner one.

    Keyword arguments:
    f -- the view which returns as an object
    '''
    def toJSONResponse(x):
        return HttpResponse(json.dumps(x), content_type = 'text/plain; charset="utf-8"')
    def g(request):
        try:
            return toJSONResponse({
                'success': True,
                'data': f(request),
            })
        except Exception as e:
            return toJSONResponse({
                'success': False,
                'type': e.__class__.__name__,
                'message': str(e),
            })
    return g

def getArgs(request):
    from django.utils.html import escape, strip_tags
    args = {}
    for k, v in list(request.POST.items()):
        if k in ('phase', 'volume'):
            args[k] = int(v)
        else:
            # NOTE strip HTML tags and escape contents
            args[k] = escape(strip_tags(v))
    return args


@require_POST
@ajaxView
def load(request):
    offset = int(request.POST['offset'])
    limit = offset + int(request.POST['limit'])
    user = request.POST['user_id']
    phase = int(request.POST['phase'])

    if offset < 0 or limit <= 0 or phase < 0 or phase > 4:
        raise ValueError('invalid interval')

    from django.contrib.auth.models import User
    try:
        user = User.objects.get(username__exact=user)
    except User.DoesNotExist:
        raise ValueError('user \'{0}\' does not exist'.format(user))
    except User.MultipleObjectsReturned:
        raise ValueError('user database corrupted')

    result = Order.objects.filter(user__exact=user, phase__exact=phase).order_by('date', 'title')[offset:limit]
    if not result:
        return None
    else:
        result = [{
            'title': x.title,
            'vendor': x.vendor,
            'date': x.date,
            'uri': x.uri,
            'thumb': '' if not x.thumb else x.thumb.url,
            'phase': x.phase,
            'volume': x.volume,
        } for x in result]
        return result

@require_POST
@login_required
@ajaxView
def save(request):
    args = getArgs(request)

    # purify keys
    args = { k: args[k] for k in ('title', 'new_title', 'vendor', 'date', 'uri', 'thumb', 'phase', 'volume') if k in args }

    # title should not be null
    if not args['title']:
        raise ValueError('`title` is empty')

    newTitle = None
    if 'new_title' in args:
        newTitle = args['new_title']
        del args['new_title']

    thumbUri = None
    if 'thumb' in args:
        thumbUri = args['thumb']
        del args['thumb']

    try:
        result = Order.objects.get(user__exact=request.user, title__exact=args['title'])
        del args['title']
        # item exists, update
        for k in args:
            setattr(result, k, args[k])
        if newTitle:
            result.title = newTitle
    except Order.DoesNotExist:
        # new item, insert
        result = Order(user=request.user, **args)
        result.retrieve_thumb(thumbUri)
    except Order.MultipleObjectsReturned:
        # TODO new exception
        raise

    result.save()
    return {
        'title': result.title,
        'vendor': result.vendor,
        'date': result.date,
        'uri': result.uri,
        'thumb': '' if not result.thumb else result.thumb.url,
        'phase': result.phase,
        'volume': result.volume,
    }

@require_POST
@login_required
@ajaxView
def move(request):
    phase = int(request.POST['phase'])
    orders = request.POST.getlist('orders[]')

    result = Order.objects.filter(title__in=orders)
    result.update(phase=phase)

    return None

@require_POST
@login_required
@ajaxView
def delete(request):
    orders = request.POST.getlist('orders[]')
    if not orders:
        raise ValueError('empty request')

    result = Order.objects.filter(title__in=orders)
    if not result:
        raise ValueError('no order matched')

    result.delete()

    return None

@login_required
def backup(request):
    from datetime import datetime
    response = HttpResponse(content_type = 'text/plain; charset="utf-8"')
    response['Content-Disposition'] = 'attachment; filename=galtrace_{0}.json'.format(datetime.now().strftime('%Y%m%d%H%M%S'))
    data = Order.objects.dump(request.user)
    json.dump(data, response, ensure_ascii=False, separators = (',', ':'))
    return response

@require_POST
@login_required
@ajaxView
def fetch(request):
    args = getArgs(request)
    result = crawler.fetch(args['uri'])
    return result
