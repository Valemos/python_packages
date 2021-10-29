import gc
import tkinter as tk


class TkContext:
    """
    use this class inside "with" syntax as shown below

    with TkContext() as context:
        *create your app with context object*

    """

    def __init__(self):
        self._tk_context: tk.Tk

    def __enter__(self):
        self._tk_context = tk.Tk()
        return self._tk_context

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tk_context.destroy()
        self._tk_context = None
        gc.collect()

