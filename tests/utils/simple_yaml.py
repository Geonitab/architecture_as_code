"""A minimal YAML loader used as a fallback when PyYAML isn't available.

The test suite relies on a small YAML configuration file that only uses a
limited subset of the YAML specification (nested mappings, lists, strings,
integers, booleans and inline lists). Installing PyYAML inside the execution
environment isn't always possible, so we provide a lightweight parser that can
handle the structures used in the project.

The implementation is intentionally conservative – it doesn't aim to support
arbitrary YAML features, but it should be resilient enough for well structured
configuration files such as the ones that ship with the repository.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Iterable, List, Tuple, Union, Any


@dataclass
class Token:
    indent: int
    content: str


class YAMLError(Exception):
    """Generic error raised when the simple YAML parser fails."""


def safe_load(text: str) -> Any:
    """Parse YAML text into Python objects using a limited subset of YAML."""
    try:
        tokens = _tokenise(text)
        if not tokens:
            return None
        return _parse(tokens)
    except Exception as exc:  # pragma: no cover - defensive programming
        raise YAMLError(str(exc)) from exc


def _tokenise(text: str) -> List[Token]:
    tokens: List[Token] = []
    for raw_line in text.splitlines():
        line = _strip_comments(raw_line)
        if not line.strip():
            continue
        if line.strip() == "---":
            # YAML document separator – safe to ignore for our use case.
            continue
        indent = len(line) - len(line.lstrip(" "))
        content = line.strip()
        tokens.append(Token(indent=indent, content=content))
    return tokens


def _strip_comments(line: str) -> str:
    """Remove YAML comments while respecting quoted strings."""
    result: List[str] = []
    in_quote = False
    quote_char = ""
    for char in line:
        if char in {'"', "'"}:
            if in_quote and char == quote_char:
                in_quote = False
                quote_char = ""
            elif not in_quote:
                in_quote = True
                quote_char = char
        if char == "#" and not in_quote:
            break
        result.append(char)
    return "".join(result).rstrip()


def _parse(tokens: Iterable[Token]) -> Any:
    root: Any = {}
    stack: List[Tuple[int, Any]] = [(-1, root)]
    tokens_list = list(tokens)

    for index, token in enumerate(tokens_list):
        indent, content = token.indent, token.content

        # Pop containers until we reach the parent with a smaller indent level.
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if content.startswith("- "):
            if not isinstance(parent, list):
                raise ValueError("List item found but parent is not a list")
            item_content = content[2:].strip()
            if not item_content:
                item: Any = {}
                parent.append(item)
                stack.append((indent, item))
                continue

            key, value_str, has_key = _maybe_split_key_value(item_content)
            if has_key:
                item_dict: dict[str, Any] = {}
                parent.append(item_dict)
                if value_str:
                    value = _parse_value(value_str)
                    item_dict[key] = value
                    if isinstance(value, (dict, list)):
                        stack.append((indent, value))
                stack.append((indent, item_dict))
            else:
                value = _parse_value(item_content)
                parent.append(value)
                if isinstance(value, (dict, list)):
                    stack.append((indent, value))
            continue

        key, value_str, has_key = _maybe_split_key_value(content)
        if has_key:
            if value_str == "":
                value = _initialise_container(tokens_list, index, indent)
            else:
                value = _parse_value(value_str)
            if not isinstance(parent, dict):
                raise ValueError("Key/value pair found but parent is not a mapping")
            parent[key] = value
            if isinstance(value, (dict, list)):
                stack.append((indent, value))
            continue

        # Bare values at the root level are not expected; return best effort.
        bare_value = _parse_value(content)
        if isinstance(parent, list):
            parent.append(bare_value)
        elif isinstance(parent, dict):
            raise ValueError(f"Unexpected bare value '{content}' inside mapping")
        else:
            root = bare_value
    return root


def _maybe_split_key_value(content: str) -> Tuple[str, str, bool]:
    if ":" not in content:
        return "", content, False
    if content.endswith(":"):
        key = content[:-1].strip()
        return key, "", True
    key, value = content.split(":", 1)
    return key.strip(), value.strip(), True


def _initialise_container(tokens: List[Token], index: int, indent: int) -> Union[dict, list]:
    for next_token in tokens[index + 1:]:
        if next_token.indent <= indent:
            break
        if next_token.content.startswith("- "):
            return []
        return {}
    return {}


def _parse_value(value: str) -> Any:
    if value == "":
        return ""
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none", "~"}:
        return None

    if value.startswith("[") and value.endswith("]"):
        try:
            return ast.literal_eval(value)
        except Exception:
            return value
    if value.startswith("{") and value.endswith("}"):
        try:
            return ast.literal_eval(value)
        except Exception:
            return value

    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]

    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value
