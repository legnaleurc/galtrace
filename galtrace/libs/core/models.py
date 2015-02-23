import hashlib
import os
from io import StringIO
import urllib.request, urllib.error, urllib.parse

from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.storage import get_storage_class

from PIL import Image

from galtrace.libs import crawler


PHASES = ((0, 'todo'), (1, 'get'), (2, 'opened'), (3, 'half'), (4, 'finished'))

class OrderManager(models.Manager):
    def dump(self, user):
        rows = super(OrderManager, self).filter(user__exact=user)
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
        super(OrderManager, self).filter(user__exact=user).delete()
        for row in rows:
            args = { x: row[x] for x in ('title', 'vendor', 'date', 'uri', 'phase', 'volume') }
            # FIXME dangerous, please check data
            o = Order(user=user, **args)
            o.retrieveThumb()
            o.save()
        return True

def _getImagePath(model, ext):
    name = hashlib.sha1(model.title.encode('utf-8')).hexdigest()
    path = '{0}/{1}{2}'.format(model.user.username, name, ext)
    return path

def getImageName(instance, filename):
    name, ext = os.path.splitext(filename)
    return _getImagePath(instance, ext)

def _getImage(uri):
    buffer_ = urllib.request.urlopen(uri)
    rawImage = buffer_.read()
    buffer_.close()

    buffer_ = StringIO(rawImage)
    image = Image.open(buffer_)
    image.thumbnail((128, 65536), Image.ANTIALIAS)
    buffer_.close()

    buffer_ = StringIO()
    image.save(buffer_, 'png')
    rawImage = buffer_.getvalue()
    buffer_.close()

    buffer_ = StringIO(rawImage)
    return ('tmp.png', File(buffer_))

class Order(models.Model):
    objects = OrderManager()

    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    date = models.CharField(max_length=15)
    uri = models.CharField(max_length=65535)
    thumb = models.ImageField(upload_to=getImageName, max_length=65535, null=True)
    phase = models.IntegerField()
    volume = models.IntegerField()

    def _getExistingThumb(self):
        path = _getImagePath(self, '.png')
        cls = get_storage_class()
        storage = cls()
        if not storage.exists(path):
            return None
        return path

    def retrieveThumb(self, uri=None):
        name = self._getExistingThumb()
        if name:
            self.thumb.name = name
            return True

        if not uri:
            try:
                siteData = crawler.fetch(self.uri)
            except crawler.UnsupportedLinkError:
                siteData = {}
            uri = siteData.get('thumb', None)
            if not uri:
                return False

        name, file_ = _getImage(uri)
        self.thumb.save(name, file_)

        return True
