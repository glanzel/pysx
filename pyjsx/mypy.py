from mypy.plugin import Plugin


class PyJSXPlugin(Plugin):
    import pyjsx.auto_setup  # type: ignore[import-unused]


def plugin(_version: str) -> type[Plugin]:
    return PyJSXPlugin
