__all__: list[str] = [
    "BaseYALError",
]


class BaseYALError(Exception):
    def __init__(
        self, message: str, class_name: str = "", function_name: str = ""
    ) -> None:
        msg: str = f"Message: {message}\nClass Name: {class_name}\nFunction Name: {function_name}"
        super().__init__(msg)
