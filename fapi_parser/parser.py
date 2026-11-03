# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod
from typing import Any, TypeVar, override

from .formatter import comment_lines, sort_order


def filter_strings_only(list: list[Any]):
    return [item for item in list if isinstance(item, str)]


class LuaConstruct(ABC):
    name: str
    description: str

    def __init__(self, obj: dict[str, Any]) -> None:
        self.name = obj.get("name") or ""
        self.description = obj.get("description") or ""

    @abstractmethod
    def format(self, options: None = None) -> str:
        """Returns a formatted version of the construct in Lua type annotation
        format"""
        # Note: options being None is a placeholder and configuring formatting will be
        # done later


T = TypeVar("T", bound=LuaConstruct)


def parse_object_list(obj: list[Any], construct: type[T]) -> list[T]:
    """Parse the list obj with class construct"""
    if not obj:
        return []

    objects = obj
    sort_order(objects)

    # more descriptive annotation maybe
    lua_constructs: list[T] = []
    for _obj in objects:
        # expected 0 arguments
        lua_constructs.append(construct(_obj))
    return lua_constructs


# attr of attributes
# - read_type OR write_type
# - optional


class LuaAttribute(LuaConstruct):
    type: str

    def __init__(self, obj: dict[str, Any]) -> None:
        super().__init__(obj)
        # 'any' is a fallback since attributes always need a type
        # make sure to change this later because
        # - "complex_type": "array"
        # - "complex_type": "table"
        # exists
        type = obj.get("read_type")
        self.type = type if isinstance(type, str) else "any"

    @override
    def format(self, options: None = None) -> str:
        filtered = filter_strings_only(
            ["@field", self.name, self.type, self.description]
        )
        return f"{comment_lines(' '.join(filtered))}"


class LuaParameter(LuaConstruct):
    type: str
    optional: bool

    def __init__(self, obj: dict[str, Any]) -> None:
        super().__init__(obj)
        type = obj.get("type")
        self.type = type if isinstance(type, str) else "any"
        self.optional = obj.get("optional") == "true"

    @override
    def format(self, options: None = None) -> str:
        filtered = filter_strings_only(
            [
                "@param",
                self.name,
                self.type + "?" if self.optional else self.type,
                self.description,
            ]
        )
        return f"{comment_lines(' '.join(filtered))}"


class LuaReturnValue(LuaConstruct):
    type: str

    def __init__(self, obj: dict[str, Any]) -> None:
        super().__init__(obj)
        self.type = obj.get("type") or ""

    @override
    def format(self, options: None = None) -> str:
        filtered = filter_strings_only(
            ["@return", self.type, "value", self.description]
        )
        return f"{comment_lines(' '.join(filtered))}"


class LuaMethod(LuaConstruct):
    """Technically methods can be either static (.) or instance (:), but
    Factorio's API does not differentiate. There are only static methods."""

    parent: str | None
    parameters: list[LuaParameter]
    return_values: list[LuaReturnValue]

    def __init__(self, obj: dict[str, Any], parent: str | None = None) -> None:
        super().__init__(obj)
        self.parent = parent
        self.parameters = parse_object_list(obj.get("parameters") or [], LuaParameter)
        self.return_values = parse_object_list(
            obj.get("return_values") or [], LuaReturnValue
        )

    @override
    def format(self, options: None = None) -> str:
        function_name = f"{self.parent}.{self.name}" if self.parent else self.name
        formatted_params = "".join(
            [parameter.format() for parameter in self.parameters]
        )
        literal_params = ", ".join([parameter.name for parameter in self.parameters])
        formatted_return_values = "".join(
            [return_value.format() for return_value in self.return_values]
        )
        return (
            f"{comment_lines(self.description)}"
            f"{formatted_params}"
            f"{formatted_return_values}"
            f"function {function_name}({literal_params}) end\n"
        )


# attr of classes
# - abstract
# - operators


class LuaClass(LuaConstruct):
    methods: list[LuaMethod]
    attributes: list[LuaAttribute]

    def __init__(self, obj: dict[str, Any]) -> None:
        super().__init__(obj)
        methods = obj.get("methods") or []
        sort_order(methods)
        self.methods = [LuaMethod(method, parent=self.name) for method in methods]
        self.attributes = parse_object_list(obj.get("attributes") or [], LuaAttribute)

    @override
    def format(self, options: None = None) -> str:
        class_declaration = comment_lines(f"@class {self.name}\n{self.description}")
        class_attributes = "".join(
            [attribute.format() for attribute in self.attributes]
        )
        class_literal = f"local {self.name} = {{}}\n"
        class_methods = "\n".join([method.format() for method in self.methods])
        return f"{class_declaration}{class_attributes}{class_literal}{class_methods}"


def parse_json(obj: dict[str, Any]):
    try:
        ## General Metadata
        # application = obj["application"]
        # application_version = obj["application_version"]
        # api_version = obj["api_version"]
        # stage = obj["stage"]

        # Nested
        lua_classes = parse_object_list(obj["classes"] or [], LuaClass)
        with open("classes.d.lua", "w", encoding="utf-8") as f:
            f.write("\n\n".join([lua_class.format() for lua_class in lua_classes]))
        # lua_globals = parse_object_list(obj["globals"])
        # lua_concepts = parse_object_list(obj["concepts"])
        # lua_global_functions = parse_object_list(obj["global_functions"])
        # lua_defines = parse_object_list(obj["defines"])
    except KeyError as e:
        # expect the entire json to be squeaky clean
        # would rather not assume it's okay every time
        print(f"error parsing json: invalid format:\n{e}")
