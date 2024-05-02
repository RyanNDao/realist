import psycopg
from psycopg.types.json import Jsonb
import logging

LOGGER = logging.getLogger(__name__)

class ModelAttribute():

    def __init__(self, type: type | tuple[type], optional: bool, validators: tuple[callable]=()):
        self.type = type
        self.validators = validators
        self.optional = optional

    def __set_name__(self, owner, name):
          self.name = name

    def __get__(self, instance, owner):
        return self if not instance else instance.__dict__[self.name]

    def __delete__(self, instance):
        del instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.type) and not (self.optional and isinstance(value, (type(None), ModelAttribute))):
            raise TypeError(f"Unable to set value because {self.name} values "
                f"{'are not optional and ' if not self.optional else ''}"
                f"must be of type {self.type!r}. "
                f"Instead, it is {type(value) if not isinstance(value, ModelAttribute) else 'empty!'}.")
        for validator in self.validators:
            validator(self.name, value)
        if isinstance(value, (list, dict)):
            value = self.castToJsonB(value)
        instance.__dict__[self.name] = value


    @staticmethod
    def castToJsonB(value):
        return Jsonb(value)