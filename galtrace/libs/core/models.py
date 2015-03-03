import hashlib
import os
import io
import urllib.request
from concurrent.futures.thread import ThreadPoolExecutor

from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.storage import get_storage_class
from PIL import Image

from galtrace.libs import crawler


PHASES = ((0, 'todo'), (1, 'get'), (2, 'opened'), (3, 'half'), (4, 'finished'))


class OrderManager(models.Manager):

    def dump(self, user):
        rows = self.filter(user__exact=user)
        orders = []
        for row in rows:
            orders.append({
                'title': row.title,
                'vendor': row.vendor,
                'date': row.date,
                'uri': row.uri,
                'phase': row.phase,
                'volume': row.volume,
            })
        data = {
            'version': 1,
            'orders': orders,
        }
        return data

    def restore(self, user, data):
        if data['version'] != 1:
            return False
        rows = data['orders']
        self.filter(user__exact=user).delete()

        with ThreadPoolExecutor(max_workers=8) as pool:
            futures = pool.map(lambda o: download_thumbnail(user, o), rows)
            orders = [order for order, thumb_ok in futures]

        for order in orders:
            order.save()

        return True

    def pull_thumbnail(self, user=None):
        if not user:
            rows = self.all()
        else:
            rows = self.filter(user__exact=user)

        with ThreadPoolExecutor(max_workers=8) as pool:
            futures = pool.map(lambda o: download_thumbnail(user, o), rows)
            for order, thumb_ok in futures:
                order.save()

        return True


def download_thumbnail(user, order):
    # `order` may be a json object or django model
    if isinstance(order, models.Model):
        args = {x: getattr(order, x) for x in ('title', 'vendor', 'date', 'uri', 'phase', 'volume')}
    else:
        args = {x: order[x] for x in ('title', 'vendor', 'date', 'uri', 'phase', 'volume')}

    if not user:
        user = order.user

    try:
        o = Order.objects.get(user__exact=user, title__exact=args['title'])
        del args['title']
        # item exists, update
        for k in args:
            setattr(o, k, args[k])
    except Order.DoesNotExist:
        # new item, insert
        o = Order(user=user, **args)
    except Order.MultipleObjectsReturned:
        # TODO new exception
        raise

    thumb_ok = o.retrieve_thumb()
    return (o, thumb_ok)


def get_image_path(model, ext):
    name = hashlib.sha1(model.title.encode('utf-8')).hexdigest()
    path = '{0}/{1}{2}'.format(model.user.username, name, ext)
    return path


def get_image_name(instance, filename):
    name, ext = os.path.splitext(filename)
    return get_image_path(instance, ext)


def get_image(uri):
    buffer_ = urllib.request.urlopen(uri)
    rawImage = buffer_.read()
    buffer_.close()

    buffer_ = io.BytesIO(rawImage)
    image = Image.open(buffer_)
    image.thumbnail((128, 65536), Image.ANTIALIAS)
    buffer_.close()

    buffer_ = io.BytesIO()
    image.save(buffer_, 'png')
    rawImage = buffer_.getvalue()
    buffer_.close()

    buffer_ = io.BytesIO(rawImage)
    return ('tmp.png', File(buffer_))


class Order(models.Model):

    objects = OrderManager()

    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    date = models.CharField(max_length=15)
    uri = models.CharField(max_length=65535)
    thumb = models.ImageField(upload_to=get_image_name, max_length=65535, null=True)
    phase = models.IntegerField()
    volume = models.IntegerField()

    def _get_existing_thumb(self):
        path = get_image_path(self, '.png')
        cls = get_storage_class()
        storage = cls()
        if not storage.exists(path):
            return None
        return path

    def retrieve_thumb(self, uri=None):
        name = self._get_existing_thumb()
        if name:
            self.thumb.name = name
            return True

        if not uri:
            try:
                site_data = crawler.fetch(self.uri)
            except (crawler.UnsupportedLinkError, crawler.UnavailableLinkError):
                site_data = {}
            uri = site_data.get('thumb', None)
            if not uri:
                return False

        name, file_ = get_image(uri)
        self.thumb.save(name, file_, save=False)

        return True
