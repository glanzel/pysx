from __future__ import annotations

from typing import Any, Protocol, TypeAlias

from pyjsx.elements import is_void_element
from pyjsx.util import flatten, indent


__all__ = ["jsx"]


class JSXComponent(Protocol):
    __name__: str

    def __call__(self, *, children: list[JSX], **rest: Any) -> JSX: ...


class JSXFragment(Protocol):
    __name__: str

    def __call__(self, *, children: list[JSX], **rest: Any) -> list[JSX]: ...


class JSXElement(Protocol):
    def __str__(self) -> str: ...


def _format_css_rule(key: str, value: Any) -> str:
    return f"{key}: {value}"


def _preprocess_props(props: dict[str, Any]) -> dict[str, Any]:
    if (style := props.get("style")) and isinstance(style, dict):
        props["style"] = "; ".join(_format_css_rule(k, v) for k, v in style.items() if v is not None)
    return props


def _render_prop(key: str, value: Any) -> str:
    if isinstance(value, bool):
        return key if value else ""
    value = str(value).replace('"', "&quot;")
    return f'{key}="{value}"'


def _render_props(props: dict[str, Any]) -> str:
    not_none = {k: v for k, v in props.items() if v is not None}
    return " ".join([_render_prop(k, v) for k, v in not_none.items()])


class _JSXElement:
    def __init__(
        self,
        tag: str | JSXComponent | JSXFragment,
        props: dict[str, Any],
        children: list[JSX],
    ):
        self.tag = tag
        self.props = props
        self.children = children

    def __repr__(self):
        tag = self.tag if isinstance(self.tag, str) else self.tag.__name__
        return f"<{tag} />"

    def __str__(self):
        match self.tag:
            case str():
                return self.convert_builtin(self.tag)
            case _:
                return self.convert_component(self.tag)

    def convert_builtin(self, tag: str) -> str:
        props = _render_props(self.props)
        if props:
            props = f" {props}"
        children = [child for child in flatten(self.children) if child is not None]
        if not children:
            if is_void_element(tag):
                return f"<{tag}{props} />"
            return f"<{tag}{props}></{tag}>"
        children_formatted = "\n".join(indent(str(child)) for child in children)
        return f"<{tag}{props}>\n{children_formatted}\n</{tag}>"

    def convert_component(self, tag: JSXComponent | JSXFragment) -> str:
        rendered = tag(**self.props, children=self.children)
        match rendered:
            case tuple() | list():
                return "\n".join(str(child) for child in rendered)
            case _:
                return str(rendered)


class _JSX:
    def __call__(
        self,
        tag: str | JSXComponent | JSXFragment,
        props: dict[str, Any],
        children: list[JSX],
    ) -> JSXElement:
        if not isinstance(tag, str) and not callable(tag):
            msg = f"Element type is invalid. Expected a string or a function but got: {tag!r}"
            raise TypeError(msg)
        props = _preprocess_props(props)
        return _JSXElement(tag, props, children)

    def Fragment(self, *, children: list[JSX], **_: Any) -> list[JSX]:
        return children


jsx = _JSX()
JSX: TypeAlias = JSXElement | str
