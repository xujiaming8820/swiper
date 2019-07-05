
class ModelToDictMixin(object):
    def to_dict(self, exclude=[]):
        attr_dict = {}

        for field in self._meta.fields:
            field_name = field.attname
            if field_name not in exclude:
                attr_dict[field_name] = getattr(self, field_name)

        return attr_dict
