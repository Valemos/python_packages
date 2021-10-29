from abc import ABCMeta, abstractmethod

from .entry_with_label import EntryWithLabel


class EntryValidatorWithLabel(EntryWithLabel, metaclass=ABCMeta):

    def __init__(self, root, label, width, fallback_value):
        super().__init__(root, label, width)
        self._fallback_value = fallback_value

    @property
    @abstractmethod
    def convert_function(self):
        """
        must return function to convert string to a specific value widget must hold
        if conversion fails function should raise ValueError
        """
        pass

    def update_field(self):
        if super().get() == "": return
        try:
            self.convert_function(super().get())
        except ValueError:
            super().set(self._fallback_value)

    def get(self):
        self.update_field()
        try:
            return self.convert_function(super().get())
        except ValueError:
            return self._fallback_value

    def set(self, value):
        super().set(str(value))
