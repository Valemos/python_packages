from pathlib import Path

from entry.entry_validator_with_label import EntryValidatorWithLabel


class EntryExistingPath(EntryValidatorWithLabel):
    def __init__(self, root, label, width, default_path: Path):
        super().__init__(root, label, width, default_path)

    @property
    def convert_function(self):
        return Path

    def get(self) -> Path:
        try:
            path = self.convert_function(super().get())
            if path.is_dir(): raise ValueError

            if not path.exists():
                path.parent.mkdir(parents=True)
                path.touch()
            return path
        except Exception:
            return self._fallback_value

    def set(self, value):
        super().set(value)