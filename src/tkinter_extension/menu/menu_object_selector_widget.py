from typing import Union

from .menu_with_handler_widget import MenuWithHandlerWidget


class MenuObjectSelectorWidget(MenuWithHandlerWidget):
    def __init__(self, root, width, choices: Union[list, dict[str, any]] = None):
        if isinstance(choices, list):
            self._choice_mapping = {str(c): c for c in choices}
        if isinstance(choices, dict):
            self._choice_mapping = choices
        if choices is None:
            self._choice_mapping = {}

        super().__init__(root, width, list(self._choice_mapping.keys()), self._handle_object_selected)

        self._selected_object = None

    def set(self, new_choice):
        for choice_name, choice in self._choice_mapping.items():
            if choice == new_choice:
                self.choose_name(choice_name)
                return
        raise ValueError("unknown object selected")

    def get(self):
        return self._selected_object

    def set_objects(self, objects, labels=None):
        if labels is None:
            self._choice_mapping = {str(obj): obj for obj in objects}
        else:
            self._choice_mapping = {lab: obj for lab, obj in zip(labels, objects)}

        self.update_choices(list(self._choice_mapping.keys()))

    def _handle_object_selected(self, selected: str):
        self._selected_object = self._choice_mapping[selected]
