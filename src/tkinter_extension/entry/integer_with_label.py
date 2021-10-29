from entry.entry_validator_with_label import EntryValidatorWithLabel


class EntryIntegerWithLabel(EntryValidatorWithLabel):

    def __init__(self, root, label, width, fallback_value=0):
        super().__init__(root, label, width, fallback_value)

    @property
    def convert_function(self):
        return int

    def get(self) -> int:
        return super().get()

    def set(self, value: int):
        super().set(value)