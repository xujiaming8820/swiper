from django.db import models
from django.core.cache import cache

from common import config


# class ModelToDictMixin(object):
def to_dict(self, exclude=[]):
    attr_dict = {}

    for field in self._meta.fields:
        field_name = field.attname
        if field_name not in exclude:
            attr_dict[field_name] = getattr(self, field_name)

    return attr_dict


def get(cls, *args, **kwargs):
    """
    为 objects 管理类的 get 方法增加缓存功能
    Model.get(pk=123)
    :param self:
    :param args:
    :param kwargs:
    :return:
    """
    # 1、从缓存中获取数据

    # 根据 pk 或 id 字段获得模型主键
    if 'pk' in kwargs:
        pk = kwargs.get('pk')
    else:
        pk = kwargs.get('id')

    if pk is not None:
        # 根据主键生成的 key，从缓存中获得数据
        key = config.MODEL_CACHE_PREFIX % (cls.__name__, pk)
        model_obj = cache.get(key)

        # 如果缓存中不为空，则返回，否则执行原有数据库操作
        if isinstance(model_obj, cls):
            return model_obj

    # 2、如果缓存中不存在，则从数据库中获得数据
    model_obj = cls.objects.get(*args, **kwargs)

    # 3、将数据库中返回的数据保存至缓存
    key = config.MODEL_CACHE_PREFIX % (cls.__name__, model_obj.pk)
    cache.set(key, model_obj)

    return model_obj


def get_or_create(cls, defaults=None, **kwargs):
    """
    为 objects 管理类的 get_or_create 增加缓存操作
    User.get_or_create()
    :param cls:
    :param defaults:
    :param kwargs:
    :return:
    """
    # 根据 pk 或 id 字段获得模型主键
    if 'pk' in kwargs:
        pk = kwargs.get('pk')
    else:
        pk = kwargs.get('id')

    if pk is not None:
        # 根据主键生成的 key，从缓存中获得数据
        key = config.MODEL_CACHE_PREFIX % (cls.__name__, pk)
        model_obj = cache.get(key)

        # 如果缓存中不为空，则返回，否则执行原有数据库操作
        if isinstance(model_obj, cls):
            return model_obj, False

    model_obj, created = cls.objects.get_or_create(defaults=None, **kwargs)

    key = config.MODEL_CACHE_PREFIX % (cls.__name__, model_obj.pk)
    cache.set(key, model_obj)

    return model_obj, created


def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    # 使用 models.Model 原有的实例方法保存数据
    self._save(force_insert=False, force_update=False, using=None,
               update_fields=None)

    # 将实例保存到缓存
    key = config.MODEL_CACHE_PREFIX % (self.__class__.__name__, self.pk)
    cache.set(key, self)


def path_model():
    models.Model.get = classmethod(get)
    models.Model.get_or_create = classmethod(get_or_create)

    models.Model._save = models.Model.save
    models.Model.save = save

    models.Model.to_dict = to_dict
