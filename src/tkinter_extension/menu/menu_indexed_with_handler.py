from .menu_with_handler_widget import MenuWithHandlerWidget


class MenuIndexedWithHandler(MenuWithHandlerWidget):

    def __init__(self, root, width, handler):
        super().__init__(self, root, width, handler)

    @staticmethod
    def indexed_name(index, name):
        return f"{index}.{name}" if name != '' else f"{index}"

    def update_choices(self, new_choices: list):
        if new_choices is not None:
            new_choices = [self.indexed_name(index + 1, name) for index, name in enumerate(new_choices)]

        super().update_choices(new_choices)

    def set_indexed_name(self, index, name):
        super().set_string(self.indexed_name(index, name) if name is not None else None)
