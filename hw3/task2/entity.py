import numpy as np
import os
import numbers
from numpy.lib.mixins import NDArrayOperatorsMixin


class PrettyPrintableMixin:
    """pretty printing in the console"""
    def __str__(self):
        result = [f"{self.__class__.__name__}("]
        properties = {}

        # collect direct attributes
        for attr in dir(self):
            # not protected/private and not a method
            if not attr.startswith('_') and not callable(getattr(self, attr)):
                properties[attr] = getattr(self, attr)

        # property-accessing mixin gives as '_properties' attribute -> we collect it per-key
        if hasattr(self, '_properties'):
            for key, value in self._properties.items():
                properties[key] = value

        for key, value in properties.items():
            result.append(f'\t"{key}": {value},')
        result.append(")")

        return "\n".join(result)

    def __repr__(self):
        properties = []
        for attr in dir(self):
            if not attr.startswith('_') and not callable(getattr(self, attr)):
                properties.append(f"{attr}={getattr(self, attr)}")
        if hasattr(self, '_properties'):
            for key, value in self._properties.items():
                properties.append(f"{key}={value}")

        return f"{self.__class__.__name__}({', '.join(properties)})"


class InFileSavableMixin:
    """saving objects in a file"""
    def save_to_file(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            f.write(str(self))
        return filename


class PropertyAccessMixin:
    """
    getters and setters for class fields.
    thin proxy for property creation and extraction
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._properties = {}

    def __getattr__(self, name):
        if name in self._properties:
            return self._properties[name]
        raise AttributeError(f"{self.__class__.__name__} has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name == '_properties':
            # don't override our own attribute
            super().__setattr__(name, value)
        else:
            self._properties[name] = value


class Entity(NDArrayOperatorsMixin, PrettyPrintableMixin, InFileSavableMixin, PropertyAccessMixin):
    """standard arithmetic operations and some other functionality through mixins."""
    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __init__(self, data):
        super().__init__()
        if isinstance(data, np.ndarray):
            self.data = data
        else:
            self.data = np.array(data)

    def __array__(self):
        return self.data

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        if method == '__call__':
            inputs = tuple(x.data if isinstance(x, Entity) else x for x in inputs)
            result = ufunc(*inputs, **kwargs)
            return Entity(result)
        else:
            return NotImplemented
