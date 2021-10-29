from entry.entry_validator_with_label import EntryValidatorWithLabel


class EntryFloatWithLabel(EntryValidatorWithLabel):
    def __init__(self, root, label, width):
        super().__init__(root, label, width, 0.0)

    @property
    def convert_function(self):
        return float

    def get(self) -> float:
        return super().get()

    def set(self, value: float):
        super().set(value)

    def set_raw(self, value):
        super().set(value)