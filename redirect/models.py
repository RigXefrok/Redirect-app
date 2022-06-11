from asyncio.windows_events import NULL
from async_timeout import timeout
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.cache import cache
# Create your models here.


class Redirect(models.Model):
    _key = models.CharField(max_length=50)
    _url = models.CharField(max_length=50)
    _active = models.BooleanField()
    _created_date = models.DateTimeField(auto_now_add=True)
    _modified_date = models.DateTimeField(auto_now=True)

    def get_redirect(self, key):
        if key == self._key:
            return {"url": self._url,
                    "created_at": self._created_date,
                    "modified_date": self._modified_date
                    }
        else:
            return None


@receiver(post_save, sender=Redirect)
def actualizar_cache(sender, instance, **kwargs):
    if instance._active:
        key = instance._key
        data = instance.get_redirect(key)
        if data:
            cache.set(key, data, timeout=None)
    else:
        cache.delete(instance._key)
